var AuraVision = (function () {
    'use strict';

    var textDisplay, statusDot, statusText, langLabel, mainCard,
        historyList, emptyHistory, visualizer, micSelect, audioLevel;

    var currentLang = 'en';
    var transcriptLog = [];
    var socket = null;
    var audioContext = null;
    var analyser = null;
    var micStream = null;
    var levelBars = [];

    var LANG_NAMES = { en: 'English', es: 'Spanish', fa: 'Farsi', unknown: 'Unknown' };

    function init() {
        textDisplay = document.getElementById('text-display');
        statusDot = document.getElementById('status-dot');
        statusText = document.getElementById('status-text');
        langLabel = document.getElementById('lang-label');
        mainCard = document.getElementById('main-card');
        historyList = document.getElementById('history-list');
        emptyHistory = document.getElementById('empty-history');
        visualizer = document.getElementById('visualizer');
        micSelect = document.getElementById('mic-select');
        audioLevel = document.getElementById('audio-level');

        createVisualizerBars();
        createLevelBars();
        setupSocket();
        setupMicSelector();
        setLang('en');
    }

    function createVisualizerBars() {
        for (var i = 0; i < 24; i++) {
            var bar = document.createElement('div');
            bar.className = 'viz-bar';
            visualizer.appendChild(bar);
        }
    }

    function createLevelBars() {
        for (var i = 0; i < 12; i++) {
            var bar = document.createElement('div');
            bar.className = 'bar';
            audioLevel.appendChild(bar);
            levelBars.push(bar);
        }
    }

    function setupSocket() {
        socket = io();

        socket.on('connect', function () {
            statusDot.className = 'status-dot connected';
            statusText.textContent = 'Connected';
            visualizer.classList.add('active');
            animateVisualizer();
        });

        socket.on('disconnect', function () {
            statusDot.className = 'status-dot';
            statusText.textContent = 'Disconnected';
            visualizer.classList.remove('active');
        });

        socket.on('lang_change', function (data) {
            setLang(data.lang);
        });

        socket.on('partial_text', function (data) {
            var text = data.text;
            var lang = data.lang || currentLang;
            if (lang !== currentLang) setLang(lang);
            textDisplay.innerHTML = '<span class="text-line partial">' + escapeHtml(text) + '</span>';
        });

        socket.on('update_text', function (data) {
            var text = data.text;
            var lang = data.lang || currentLang;
            if (lang !== currentLang) setLang(lang);
            textDisplay.innerHTML = '<span class="text-line">' + escapeHtml(text) + '</span>';
            mainCard.classList.add('active');
            setTimeout(function () { mainCard.classList.remove('active'); }, 1500);
            addHistory(text, lang);
        });
    }

    function setupMicSelector() {
        fetch('/mics')
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (!data.mics || data.mics.length === 0) return;
                micSelect.innerHTML = '';
                data.mics.forEach(function (m) {
                    var opt = document.createElement('option');
                    opt.value = m.index;
                    opt.textContent = m.name + ' (' + m.channels + 'ch)';
                    micSelect.appendChild(opt);
                });
                if (data.default >= 0) {
                    micSelect.value = data.default;
                }
                startMicLevel(data.default >= 0 ? data.default : data.mics[0].index);
            })
            .catch(function () {
                document.getElementById('mic-section').style.display = 'none';
            });

        micSelect.addEventListener('change', function () {
            var idx = parseInt(micSelect.value, 10);
            startMicLevel(idx);
            if (socket && socket.connected) {
                socket.emit('set_mic', { mic_index: idx });
            }
        });
    }

    function startMicLevel(deviceIndex) {
        if (micStream) {
            micStream.getTracks().forEach(function (t) { t.stop(); });
        }
        if (audioContext) {
            audioContext.close();
        }

        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 64;

        navigator.mediaDevices.getUserMedia({
            audio: { deviceId: { exact: deviceIndex } }
        }).then(function (stream) {
            micStream = stream;
            var source = audioContext.createMediaStreamSource(stream);
            source.connect(analyser);
            updateLevelLoop();
        }).catch(function () {
            document.getElementById('mic-section').style.display = 'none';
        });
    }

    function updateLevelLoop() {
        if (!analyser) return;
        var data = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(data);

        var sum = 0;
        for (var i = 0; i < data.length; i++) sum += data[i];
        var avg = sum / data.length;
        var normalized = Math.min(avg / 128, 1);

        for (var j = 0; j < levelBars.length; j++) {
            var threshold = j / levelBars.length;
            if (normalized > threshold) {
                var h = Math.max(4, normalized * 20);
                levelBars[j].style.height = h + 'px';
                levelBars[j].classList.toggle('hot', j >= levelBars.length - 3 && normalized > 0.7);
            } else {
                levelBars[j].style.height = '4px';
                levelBars[j].classList.remove('hot');
            }
        }

        requestAnimationFrame(updateLevelLoop);
    }

    function animateVisualizer() {
        if (!visualizer.classList.contains('active')) return;
        var bars = visualizer.querySelectorAll('.viz-bar');
        bars.forEach(function (bar) {
            bar.style.height = (Math.random() * 24 + 4) + 'px';
        });
        requestAnimationFrame(function () {
            setTimeout(animateVisualizer, 100);
        });
    }

    function setLang(lang) {
        currentLang = lang;
        var isRtl = lang === 'fa';
        textDisplay.className = 'text-area ' + (isRtl ? 'rtl' : 'ltr');
        langLabel.textContent = LANG_NAMES[lang] || lang;
        document.documentElement.lang = isRtl ? 'fa' : 'en';
    }

    function timeNow() {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }

    function addHistory(text, lang) {
        if (emptyHistory) emptyHistory.style.display = 'none';
        var item = document.createElement('div');
        item.className = 'history-item' + (lang === 'fa' ? ' rtl' : '');
        item.setAttribute('role', 'listitem');
        item.innerHTML = '<div>' + escapeHtml(text) + '</div><div class="time">' + timeNow() + '</div>';
        historyList.prepend(item);

        transcriptLog.unshift({ text: text, lang: lang, time: Date.now() });
        if (transcriptLog.length > 100) {
            transcriptLog.pop();
            if (historyList.lastChild && historyList.lastChild.id !== 'empty-history') {
                historyList.removeChild(historyList.lastChild);
            }
        }
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function clearHistory() {
        transcriptLog = [];
        historyList.innerHTML = '';
        if (emptyHistory) {
            historyList.appendChild(emptyHistory);
            emptyHistory.style.display = '';
        }
    }

    function exportHistory() {
        if (transcriptLog.length === 0) return;
        var lines = transcriptLog.slice().reverse().map(function (entry) {
            var t = new Date(entry.time).toLocaleString();
            return '[' + t + '] (' + (LANG_NAMES[entry.lang] || entry.lang) + ') ' + entry.text;
        });
        var blob = new Blob([lines.join('\n')], { type: 'text/plain' });
        var a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'auravision-transcript.txt';
        a.click();
        URL.revokeObjectURL(a.href);
    }

    document.addEventListener('DOMContentLoaded', init);

    return { clearHistory: clearHistory, exportHistory: exportHistory };
})();
