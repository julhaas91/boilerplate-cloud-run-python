# Set Up Workload Identity Federation for GitHub Actions

When deploying services on the open web, secure authentication is crucial. The simplest method for Google Cloud authentication is using service account key files, but they pose a security risk—keys don’t expire and can be misused if exposed.

To mitigate this, we use [**Workload Identity Federation (WIF)**](https://cloud.google.com/iam/docs/workload-identity-federation), which replaces long-lived keys with short-lived access tokens.

We can provide **keyless** access to Google Cloud resources via [Workload Identity Federation (WIF)](https://cloud.google.com/iam/docs/workload-identity-federation) for AWS, Azure, on-prem AD, GitHub, GitLab, and any identity provider (IdP) that supports either:
1. OpenID Connect (**OIDC**) or
2. Security Assertion Markup Language (**SAML**) V2.0

There are two ways of using WIF ([source](https://github.com/google-github-actions/auth?tab=readme-ov-file#direct-wif)):

1. **Direct WIF** – Grants IAM permissions directly to the Workload Identity Pool, removing the need for service accounts or keys. Faster but limited to supported Google Cloud services.
2. **WIF via service account impersonation** – The Workload Identity Pool impersonates a service account, ensuring broader compatibility by inheriting its permissions.

## Setup 

In the following steps, we set up WIF to integrate a GitHub Actions CI/CD pipeline with Google Cloud ([source](https://github.com/google-github-actions/auth?tab=readme-ov-file#preferred-direct-workload-identity-federation)).

```bash
export PROJECT_ID="YOUR-PROJECT-ID" 
export GITHUB_ORG="YOUR-GITHUB-ORG"
export REPO_NAME="YOUR-REPO-NAME"
```
### Create WIF Pool

First, we create a Workload Identity Federation (WIF) pool, which serves as the authentication bridge between GitHub Actions and Google Cloud.

``` bash
gcloud iam workload-identity-pools create "github" \
--project="${PROJECT_ID}" \
--location="global" \
--display-name="GitHub Actions Pool"
```
_**Note**: The only supported location is "global" ([source](https://cloud.google.com/iam/docs/reference/rest/v1/projects.locations.workloadIdentityPools/create)), as WIF is a [global product](https://cloud.google.com/about/locations#global-products) replicated across regions._

### Create WIF Provider

Next, we create a WIF provider within the pool, which validates GitHub's OpenID Connect (OIDC) tokens and maps attributes for authentication.

``` bash
gcloud iam workload-identity-pools providers create-oidc "my-repo" \
--project="${PROJECT_ID}" \
--location="global" \
--workload-identity-pool="github" \
--display-name="My GitHub repo Provider" \
--attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
--attribute-condition="assertion.repository_owner == '${GITHUB_ORG}'" \
--issuer-uri="https://token.actions.githubusercontent.com"
```

### Get WIF Provider Resource Name

Then, we retrieve the WIF provider resource name, which is required for configuring authentication in the GitHub Actions workflow.

``` bash
gcloud iam workload-identity-pools providers describe "my-repo" \
--project="${PROJECT_ID}" \
--location="global" \
--workload-identity-pool="github" \
--format="value(name)"
```

### Use the WIF provider resource name in the GitHub Actions YAML

We configure GitHub Actions to use the WIF provider by referencing its resource name within the workflow YAML file.

``` yaml
jobs:
  job_id:
    runs-on: ubuntu-latest

    permissions:
      contents: 'read'
      id-token: 'write'

    steps:
    - uses: 'actions/checkout@v4'

    - uses: 'google-github-actions/auth@v2'
      with:
        project_id: 'YOUR-PROJECT-ID'
        workload_identity_provider: 'YOUR-WIF-PROVIDER-RESOURCE-NAME'
```

### Get WIF Pool ID

We retrieve the WIF pool ID, which is necessary for assigning permissions to the pool.

``` bash
gcloud iam workload-identity-pools describe "github" \
--project="${PROJECT_ID}" \
--location="global" \
--format="value(name)"
```

_**Note**: the only supported location is "global" ([SOURCE](https://cloud.google.com/iam/docs/reference/rest/v1/projects.locations.workloadIdentityPools/create)), as WIF is a [global product](https://cloud.google.com/about/locations#global-products) replicated over the regions._

### Set permissions

We now assign the necessary IAM roles to allow GitHub Actions to interact with Google Cloud resources securely using WIF.

#### Export Export Environment Variables

We export necessary environment variables to simplify command execution in subsequent steps.

``` bash
export WORKLOAD_IDENTITY_POOL_ID="YOUR-WIF-IDENTITY-POOL-ID"
```
#### Grant Access to Secrets

We grant the WIF pool permission to access secret values stored in Secret Manager.

``` bash
gcloud secrets add-iam-policy-binding "my-secret" \
  --project="${PROJECT_ID}" \
  --role="roles/secretmanager.secretAccessor" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_ORG}/${REPO_NAME}"
```
#### Grant Access to Push Docker Containers

We create an Artifact Registry repository to store Docker images used for deployment.

```bash
gcloud artifacts repositories create docker \
  --repository-format=docker \
  --location="europe-west3" \
  --description="Docker container registry for my project" \
  --project="${PROJECT_ID}" 
```
_See [documentation](https://cloud.google.com/sdk/gcloud/reference/artifacts/repositories/create) for more information on the `gcloud artifacts repositories create` command._

``` bash
gcloud artifacts repositories add-iam-policy-binding "docker" \
--location="europe-west3" \
--role="roles/artifactregistry.writer" \
--member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_ORG}/${REPO_NAME}" 
```
_See [documentation](https://cloud.google.com/sdk/gcloud/reference/artifacts/repositories/add-iam-policy-binding) for more information on the `gcloud artifacts repositories add-iam-policy-binding` command._

For direct WIF ([source](https://github.com/google-github-actions/auth?tab=readme-ov-file#direct-wif)), we grant the following permissions to our Cloud Run service account:

1. `roles/iam.workloadIdentityUser`:
    - This is the basic role that allows GitHub Actions (via Workload Identity Federation) to authenticate as our service account
    - Think of it as "permission to log in as this service account"

``` bash
gcloud iam service-accounts add-iam-policy-binding ${REPO_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/815648219579/locations/global/workloadIdentityPools/github/attribute.repository/${GITHUB_ORG}/${REPO_NAME}"
```
_See [documentation](https://cloud.google.com/sdk/gcloud/reference/iam/service-accounts/add-iam-policy-binding) for more information on the `gcloud iam service-accounts` command._

2. `roles/iam.serviceAccountUser`:
    - This role grants the specific `iam.serviceaccounts.actAs` permission
    - It's needed because Cloud Run deployment requires actually running operations as the service account
    - Think of it as "permission to do things as this service account"

```bash
gcloud iam service-accounts add-iam-policy-binding ${REPO_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
    --role="roles/iam.serviceAccountTokenCreator" \
    --member="principalSet://iam.googleapis.com/projects/815648219579/locations/global/workloadIdentityPools/github/attribute.repository/${GITHUB_ORG}/${REPO_NAME}"
```
_See [documentation](https://cloud.google.com/sdk/gcloud/reference/iam/service-accounts/add-iam-policy-binding) for more information on the `gcloud iam service-accounts` command._

3. `roles/iam.serviceAccountTokenCreator`:
    - This allows the creation of OAuth2.0 tokens for the service account
    - Cloud Run needs these tokens for its ongoing operations
    - Think of it as "permission to create credentials for this service account"

```bash
gcloud iam service-accounts add-iam-policy-binding ${REPO_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
    --role="roles/iam.serviceAccountUser" \
    --member="principalSet://iam.googleapis.com/projects/815648219579/locations/global/workloadIdentityPools/github/attribute.repository/${GITHUB_ORG}/${REPO_NAME}"
```
_See [documentation](https://cloud.google.com/sdk/gcloud/reference/iam/service-accounts/add-iam-policy-binding) for more information on the `gcloud iam service-accounts` command._

#### Grant Access to Cloud Run

Let's deploy the Cloud Run service using an image from the Artifact Registry.

``` bash
gcloud run deploy ${REPO_NAME} \
--region="europe-west3" \
--image="europe-west3-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}" \
--allow-unauthenticated 
```
**⚠ WARNING:** `--allow-unauthenticated` makes the service publicly accessible. I do not recommend this—set up [authentication](https://cloud.google.com/docs/authentication), such as [SSO](https://cloud.google.com/architecture/identity/single-sign-on) for the frontend and [OAuth 2.0](https://cloud.google.com/docs/authentication#oauth2) for backend services.

Now, we need to grant GitHub Actions permission to manage and run the Cloud Run service.

``` bash
gcloud run services add-iam-policy-binding ${REPO_NAME} \
--project="${PROJECT_ID}" \
--region="europe-west3" \
--role="roles/run.admin" \
--member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_ORG}/${REPO_NAME}"
```

_See [documentation](https://cloud.google.com/sdk/gcloud/reference/run/services/add-iam-policy-binding) for more information on the `gcloud run services add-iam-policy-binding` command._
