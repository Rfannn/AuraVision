# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest  | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT open a public issue**
2. Email: tsmrfangg@gmail.com
3. Include: description, steps to reproduce, potential impact

We will respond within 48 hours and work with you to fix the issue.

## Scope

AuraVision is designed for **local use** on a single machine. The `/update` endpoint accepts an optional `AV_AUTH_TOKEN` for basic access control when exposing the server on a network.

## Best Practices

- Use `AV_AUTH_TOKEN` when running on a shared network
- Keep `AV_DEBUG=false` in production
- Use gunicorn (not Flask dev server) for production deployments
