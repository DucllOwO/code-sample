<div align="center">
  <h1>Fullstack Authentication</h1>
</div>

**Hi, this is the codebase where I learned about refresh tokens, along with a simple websocket.**

# Stack

**Backend**: Node.js, Typescript, MongoDB

**Frontend**: Next.js, Typescript

# Usage

**Requirements**: Docker, Docker Compose, Yarn, Node.js

**Setup**

- `make setup`
- Create GitHub OAuth app [here](https://github.com/settings/developers)
  - Set "Homepage URL" to `http://localhost:3000`
  - Set "Authorization callback URL" to `http://localhost:3000/github`
  - Set `GITHUB_CLIENT_ID` in [`.env.development`](.env.development)
  - Set `NEXT_PUBLIC_GITHUB_CLIENT_ID` in [`client/.env.development`](client/.env.development)
  - "Generate a new client secret"
  - Set `GITHUB_CLIENT_SECRET` in [`.env.development`](.env.development)

# Codebase

**Services**

- [`client`](client) **Next.js client** (web application)
- [`api`](api) **Node.js server** (http api)
- [`realtime`](realtime) **Node.js server** (websocket server)
- [`shared`](shared) **Typescript lib** (shared code)
