# pico

[![Build Status](https://travis-ci.com/picoCTF/picoCTF.svg?branch=master)](https://travis-ci.com/picoCTF/picoCTF)
[![codecov](https://codecov.io/gh/picoCTF/picoCTF/branch/master/graph/badge.svg)](https://codecov.io/gh/picoCTF/picoCTF)

The pico platform is the infrastructure used to run [picoCTF](https://picoctf.com/).
It is designed to be easily adapted for other CTF or programming competitions.

If using the platform to host a custom competition, we recommend using the most recent tagged [release](https://github.com/picoCTF/picoCTF/releases). The `master` branch represents active development and may not be stable. Additionally, we cannot guarantee the stability or security of any outdated releases.

Additional documentation can be found at [docs.picoctf.com](https://docs.picoctf.com) or within the [`/docs` directory](./docs/README.md).

Please visit our Discord server for other platform deployment questions not
covered in our documentation: https://discord.gg/WQGdYaB

## Quick Start

The pico platform requires the [Docker desktop client](https://www.docker.com/products/docker-desktop).

To start, run:

```shell
docker-compose up -d
```

from this directory. The web interface will be accessible at `https://localhost:13371`.

The first user account registered will be the platform's superadmin.

Note that you will need to trust the web UI's self-signed certificate.
For information on how to use a custom certificate and other deployment options, see [Advanced Deployment](#advanced-deployment).

By default, the main database and user home directories are stored in Docker volumes which will persist across platform restarts.

## Features

The pico platform provides everything required to run CTFs and other CS-oriented competitions.

- Challenge management
  - Filterable list of challenges with optional hints
  - Enforcable challenge progression via dependencies
  - Flag validation
  - Multiple instances (versions) of challenges
  - Provided framework for easy challenge creation
- Team management
  - Configurable maximum team size
- Scoreboards
  - Supports multiple scoreboards per competition based on eligibility criteria
- Webshell
  - Players can use a browser-based Linux shell to solve challenges
- Classrooms
  - Teacher accounts can group users as students within a classroom
  - Separate scoreboards for classrooms
  - Student progress metrics for teachers

## Platform Components

See each component's README.md for additional details.

### [API](./api)

A Flask-based REST API that is the core of the platform, handling the management
of challenges, users, competitions, etc.

### [Challenges](./challenges)

Resources for creating new challenges using the provided hacksport framework.
Also includes a set of sample challenges to get started.

### [UI](./ui)

A customizable React frontend for the pico API.

### [Webshell](./webshell)

Provides on-demand containers containing a Linux shell environment and various hacking tools.
Useful for beginners and players without access to a local shell.

## Advanced Deployment

While the provided [`docker-compose.yml`](./docker-compose.yml) is likely sufficient for small deployments, additional options are available to support production-level deployments and local platform development.

### Kubernetes

*@todo provide k8s manifests and installation documentation*

### Compose Overrides

Several [override files](https://docs.docker.com/compose/extends/#multiple-compose-files) are available to facilitate common platform customizations.

To use override files, explicitly include them in your `docker-compose up` command, e.g.:

```shell
docker-compose -f docker-compose.yml [-f docker-compose.override.yml...] up -d
```

- *[.custom-ssl.yml](./docker-compose.custom-ssl.yml)*: use a custom key and certificate specified in `ui/custom_tls` for the web UI.
- *[.ports.yml](./docker-compose.ports.yml)*: expose ports on each platform component directly, rather than only the UI. Useful for local development.

## Local Development

In general, when developing the platform itself, it is easiest to test changes by simply re-running your `docker-compose up` command with the `--build` flag.

This will rebuild only components which have changed, and will generally execute very quickly due to cached dependency layers.

See each component's README.md file for additional information.

### Exposing Additional Ports

By default, only the web UI is accessible when running `docker-compose up`. When developing, it is often useful to e.g. send HTTP requests directly to the API, or access the database with an external tool. To expose additional ports on each container, include the [.ports.yml](./docker-compose.ports.yml) [Compose override](#compose-overrides) in your `docker-compose up` command.

### Basic Docker Commands

View running containers

```shell
docker ps
```

Tail a container's logs

```shell
docker logs -f container_name
```

Get a shell on a container

```shell
docker exec -it container_name bash
```

Pause all pico containers

```shell
docker-compose stop
```

Remove all pico containers/networks/volume mounts

```shell
docker-compose down
```

### Resetting the Database

To fully remove the persistent database volume and reset the platform to its initial state:

```shell
docker-compose down -v
```

## Want your own contest, but are not a developer?

[ForAllSecure](https://forallsecure.com) offers professionally-run original
hacking contests as a service.

## Giving Back and Development

The pico platform is always under development.

- See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.
- We are especially interested any improvements on continuous integration and
  automated testing.

If you are interested in research in CTFs (e.g., improving skill acquisition,
decreasing time to mastery, etc.), please feel free to email David Brumley.

## Credits

picoCTF was started by David Brumley with his CMU professor hat in 2013. The
intention has always been to give back to the CTF community.

The original heavy lifting was done by his graduate students, and special thanks
is due to Peter Chapman (picoCTF 2013 technical lead) and Jonathan Burket
(picoCTF 2014 technical lead) for their immense efforts not only developing
code, but for organizing art work, problem development, and so on.

In 2015-2016 significant effort was done by
[ForAllSecure](https://forallsecure.com) at the companies expense. This includes
adding concepts like the shell server, and rewriting significant portions of the
web server.

Both CMU and ForAllSecure have agreed to release all code under the [MIT
LICENSE](./LICENSE) . We do encourage attribution as that helps us secure
funding and interest to run picoctf year after year, but it is not
necessary. Also, if you do end up running a contest, do feel free to drop David
Brumley a line.

- Bug Reports: [GitHub Issues](https://github.com/picoCTF/picoCTF/issues)
- Contributors (in no particular order): David Brumley, Tim Becker, Chris Ganas,
  Roy Ragsdale, Peter Chapman, Jonathan Burket, Collin Petty, Tyler Nighswander,
  Garrett Barboza, Mong-Yah "Max" Hsieh
