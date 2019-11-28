# pico UI

This is a [React](https://reactjs.org/)-based UI for interacting with the **[pico API](../api)**.
It runs as its own container, served via [nginx](https://www.nginx.com/) on standard HTTPS port 443.
pico UI containers are stateless and do not require session pinning, so they can be arbitrarially horizontally scaled
and load-balanced as needed.

Additionally, the **[pico API](../api)** and **[webshell dispatcher](../webshell)** are proxied through
the UI webserver to avoid CSRF and TLS termination issues.

By default, the UI uses a self-signed certificate and key for HTTPS generated during the image build process.
In a production environment, you should replace this keypair with a trusted one containing your DNS name
(see the provided **[docker-compose override](../docker-compose.custom-ssl.yml)** for this purpose.)

## Local Development

For the purposes of local development (autocompletion, etc.), it may be useful to install
the npm dependencies using the standard **[package.json](./package.json)** file.

Building the UI is a two-step process that involves compiling the JSX source files, then using [Jekyll](https://jekyllrb.com/) to generate the final output.
While it is possible to do this locally (see the **[Dockerfile](./Dockerfile)** for reference), it is recommended
to simply rebuild the UI container within the existing docker-compose network (see the **[platform README](../README.md)** for more information).
