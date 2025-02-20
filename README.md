```plaintext                                                                                                                                                                                                                                                             

   ██████╗██╗      ██████╗ ██╗   ██╗██████╗     ██████╗ ██╗   ██╗███╗   ██╗            
  ██╔════╝██║     ██╔═══██╗██║   ██║██╔══██╗    ██╔══██╗██║   ██║████╗  ██║            
  ██║     ██║     ██║   ██║██║   ██║██║  ██║    ██████╔╝██║   ██║██╔██╗ ██║            
  ██║     ██║     ██║   ██║██║   ██║██║  ██║    ██╔══██╗██║   ██║██║╚██╗██║            
  ╚██████╗███████╗╚██████╔╝╚██████╔╝██████╔╝    ██║  ██║╚██████╔╝██║ ╚████║            
  ╚═════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝            
                                                                                     
  ██████╗  ██████╗ ██╗██╗     ███████╗██████╗ ██████╗ ██╗      █████╗ ████████╗███████╗
  ██╔══██╗██╔═══██╗██║██║     ██╔════╝██╔══██╗██╔══██╗██║     ██╔══██╗╚══██╔══╝██╔════╝
  ██████╔╝██║   ██║██║██║     █████╗  ██████╔╝██████╔╝██║     ███████║   ██║   █████╗  
  ██╔══██╗██║   ██║██║██║     ██╔══╝  ██╔══██╗██╔═══╝ ██║     ██╔══██║   ██║   ██╔══╝  
  ██████╔╝╚██████╔╝██║███████╗███████╗██║  ██║██║     ███████╗██║  ██║   ██║   ███████╗
  ╚═════╝  ╚═════╝ ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                                                  
```
### 🚀 Deploy your Cloud Run application to the Google Cloud in record time! 🚀

<details>
<summary><strong>TL;DR (Too Long; Didn't Read) 😴🥱💤</strong></summary>
First, you need to set up Workload Identity Federation by following <a href="./SETUP_WIF.md">these steps</a>.
<br><br>
Next, set the necessary environment variables in `config.env` and run the following commands:

```bash
./taskfile.sh setup_project && ./taskfile.sh run_application
```
(If you get a _permission denied_ error, run: `chmod +x ./taskfile.sh`)

</details>

## Content Overview

1. ❓ [Why do I need this boilerplate?](#why-do-I-need-this-boilerplate)

2. 👨‍💻 [Development](#development)
   - 🛠️ [Frameworks and Tools](#frameworks-and-tools)
   - ⚙️ [Setup](#setup)
   - 💡 [Application Logic](#application-logic)
   - ✅ [Validate the Application](#validate-the-application)
   - 🧪 [Test the Application](#test-the-application)

3. 🔑 [Google Cloud Authentication Prerequisites](#google-cloud-authentication-prerequisites)
   - 👤 [Local Authentication](#local-authentication)
   - 🤝 [GitHub Actions Authentication via Workload Identity Federation](#github-actions-authentication-via-workload-identity-federation)

4. ⬆️ [Deployment](#deployment)
   - 🧑‍🔧 [Manual Deployment (Local)](#manual-deployment-local)
   - 🤖 [Automated Deployment (CI/CD)](#automated-deployment-cicd)

5. 🎁 [Release Management](#release-management)
   - 📝 [Release Prerequisites](#release-prerequisites)
   - 💥 [Triggering a Release](#triggering-a-release)
   - 🔢 [Versioning](#versioning)

6. 🏃 [Execution](#execution)
   - 💻 [Run the Application Locally](#run-the-application-locally)
   - ☁️ [Run the Application in the Google Cloud](#run-the-application-in-the-google-cloud)

7. 📄 [License](#license) 
8. 📬 [Contact](https://www.linkedin.com/in/jh91/)

# Why do I need this boilerplate?
- 🚀 **Simplify Cloud Run Deployment:** Includes a ready-to-use GitHub Actions CI/CD pipeline.
- 🖱️ **One-Click Release Management:** Trigger releases with a single click in the GitHub Actions UI.
-  ⚡ **Fast Dependency & Environment Management:** Python versions, dependencies, and virtual environments managed with `uv` —10-100x faster compared to `pip`.
- 🛠️ **Quick Google Cloud Setup:** Skip complex project settings — configure all necessary Google Cloud settings with a single command.
- 🔐 **Secure, Keyless Authentication:** Supports Workload Identity Federation for seamless Google Cloud access.

Get started on building, not configuring! 💡

## Development
## Frameworks and tools

- ⭐ Built with the `Litestar` ASGI framework ([repo][litestar-repository] / [documentation][litestar-documentation]).
- 🧩 Python dependencies managed via `uv` ([repo][uv-repository] / [documentation][uv-documentation]) with a 🔒 ([`uv.lock`](./uv.lock)) file for consistency.
  - 📄 Dependencies are specified in the [`pyproject.toml`](./pyproject.toml) file ([documentation][pytoml-documentation]).
  - 🐍 The Python version is specified in the [`.python-version`](./.python-version) file.
- 🧹 Code linting and formatting by `ruff` ([repo][ruff-repository] / [documentation][ruff-documentation]). 
- 🧪 Testing handled with `pytest` ([repo][pytest-repository] / [documentation][pytest-documentation]). 
- ⚙️ Deployment to [Cloud Run][cloud-run-documentation] via CI/CD integrated with `GitHub Actions` ([documentation][gh-actions-documentation]). 
- 🏷️ Automated Release Management with `python-semantic-release` ([repo][python-semantic-release-repository] / [documentation][python-semantic-release-documentation])


### Setup

To set up your local development environment:

```bash
./taskfile.sh setup_project
```

(If you get a _permission denied_ error, run: `chmod +x ./taskfile.sh`)

### Application Logic

- ➕ To install additional packages, run [`./taskfile.sh install <package>`](taskfile.sh)
- 🐍 To change the Python version, modify [`.python-version`](.python-version)  
- 🌎 Update environment variables and critical settings (e.g., project, service accounts) in [`config.env.`](config.env.)
- ⚙️ For project-specific configurations, edit [`pyproject.toml`](pyproject.toml)
- 💻 Implement new logic in the [`src`](src) folder
- 🧪 Write tests in the [`test`](test)

### Validate the application

To validate the application, run: 

```bash
./taskfile.sh validate
```

### Test the application

To test the application, run: 

```bash
./taskfile.sh test
```

## Google Cloud Authentication Prerequisites

To set up the authentication to Google Cloud, follow these steps:

### Local Authentication

Authenticate your local environment using your user credentials:

```bash
./taskfile.sh authenticate
```

### GitHub Actions Authentication via Workload Identity Federation

Set up the authentication of GitHub Actions via Workload Identity Federation by executing <a href="./SETUP_WIF.md">these steps</a>.


## Deployment

### Manual Deployment (Local)

1. 🧑‍🔧 **Authenticate:** Connect to Google Cloud. See [Authentication to Google Cloud](#authentication-to-google-cloud) for instructions:

```bash
./taskfile.sh authenticate
```

2. ⬆️ **Deploy:** Build and push your Docker image to Google Container Registry, and deploy to Cloud Run:

```bash
./taskfile.sh deploy <GCP-PROJECT> <SERVICE-ACCOUNT>
```

### Automated Deployment (CI/CD)

The [`.github/workflows/deployment.yml`](.github/workflows/deployment.yml) workflow automates deployment on merges to the `main` branch. It can also be triggered manually via the GitHub Actions interface.

## Release Management

### Release Prerequisites

1. 🛠️ A new feature/bugfix has been developed on a feature/bugfix branch
2. 🔄 The respective feature/bugfix branch has been merged into the `main` branch via
pull request and code review.

### Triggering a Release

Releases are managed via the [`.github/workflows/release.yml`](.github/workflows/release.yml) GitHub Actions workflow. A new release can be triggered manually via the GitHub UI `https://github.com/<account>/<repository>/actions`) or running:

```bash
./taskfile.sh release
```

This updates the version number, updates `./CHANGELOG.md`, pushes changes, and tags the commit. Local release triggers are **not** recommended.

### Versioning

The version management of this boilerplate is handled using `python-semantic-release` ([repo][python-semantic-release-repository] / [documentation][python-semantic-release-documentation]), which is a Python implementation of `semantic-release` ([repo][semantic-release-repository] / [documentation][semantic-release-documentation]) for JavaScript.

`python-semantic-release` will execute the following steps:
1. 📈 A new version number will be calculated
2. ⬆️ A release commit will be pushed to the remote repo
3. 🎉 A GitHub Release will be created

> semantic-release uses commit messages to determine the consumer impact of changes in the codebase. Following formalized conventions for commit messages, semantic-release automatically determines the next [semantic version number][semantic-versioning], generates a changelog and publishes the release.
>
> [(source)[semantic-release-repository]

The semantic version number is structured as `MAJOR.MINOR.PATCH` (e.g. `2.0.11`).

This repository uses [Angular Commit Message Conventions][angular-commit-conventions]:
> **MAJOR:** triggered by *"BREAKING CHANGE:"* mentioned in the **footer** of the commit message. See [examples][angular-commit-examples].
>
> **MINOR:** triggered by *"feat"*
>
> **PATCH:** triggered by *"fix"* or *"perf"* tags in the commit message
> 
> See the [pyproject.toml](./pyproject.toml) for more details.


## Execution

### Run the application locally

To run the application locally, execute:

```bash
./taskfile.sh
```

### Run the application in the Google Cloud

After successfully deploying to Cloud Run, you can send requests to the service URL, e.g., `https://my-awesome-service-12345-uc.a.run.app/process`.
To authenticate your requests, include a [Bearer token](https://cloud.google.com/run/docs/authenticating/service-to-service#acquire-token) in the header of your REST requests. You can create a valid token by running:

```bash
./taskfile.sh create_identity_token
```

(Remember to authenticate first using `./taskfile.sh authenticate`)

> Refer to [./taskfile.sh](./taskfile.sh) for additional tasks to assist in development.

### Example usage

You can send a request using a tool like [Postman](https://www.postman.com/) for testing purposes.

**Example request**: 

```json
{
  "message": "Hi, this is a test message..."
}
```

**Example response**:

```json
{
    "uppercaseMessage": "HI, THIS IS A TEST MESSAGE..."
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

> For inquiries, feel free to contact me via [email](mailto:juliushaas91@gmail.com) or [LinkedIn](https://www.linkedin.com/in/jh91/) 


[uv-repository]: https://github.com/astral-sh/uv
[uv-documentation]: https://docs.astral.sh/uv/
[ruff-repository]: https://github.com/astral-sh/ruff
[ruff-documentation]: https://docs.astral.sh/ruff/
[litestar-repository]: https://github.com/litestar-org/litestar
[litestar-documentation]: https://docs.litestar.dev/latest/
[pytest-repository]: https://github.com/pytest-dev/pytest
[pytest-documentation]: https://docs.pytest.org/en/stable/contents.html
[python-semantic-release-repository]: https://github.com/python-semantic-release/python-semantic-release
[python-semantic-release-documentation]: https://python-semantic-release.readthedocs.io/ 
[semantic-release-repository]: https://github.com/semantic-release/semantic-release
[semantic-release-documentation]: https://semantic-release.gitbook.io/semantic-release#documentation

[cloud-run-documentation]: https://cloud.google.com/run
[gh-actions-documentation]: https://docs.github.com/en/actions

[angular-commit-conventions]: https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines
[angular-commit-examples]: https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/
[semantic-versioning]: https://semver.org/
[pytoml-documentation]: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
