# The Build and Push GitHub Action

The action builds a container image and pushes it to the specified registry.

## Action Inputs

### Registry information

| Input Name | Description | Default value |
|------------|-------------|---------------|
| `registry` | Registry to push container image to. | **required**  |
| `registry_namespace` | Namespace of the registry, where the image would be pushed. | **required**  |
| `registry_username` | Login to specified registry. | **required**  |
| `registry_token` | Access token to specified registry. | **required**  |

### Build information

| Input Name | Description | Default value |
|------------|-------------|---------------|
| `tag` | Tag of the built image. | **required** |
| `dockerfile` | Dockerfile to build the image. | Dockerfile |
| `dockerfile_path` | Path to a Dockerfile, relative to the fetched git repository root. | **required** |
| `use_distgen` | The action will use distgen for generating dockerfiles if true. | false |
| `docker_context` | Docker build context. | . |
| `suffix` | Paramater adds suffix as `-suffix` into image name | '' |



## Example

The example below shows how the `sclorg/build-and-push-action` can be used.

```yaml
name: Build and push to quay.io registry
on:
  push:
    branches:
      - main

jobs:
  build-and-push:
    runs-on: ubuntu-20.04
    steps:
      - name: Build and push to quay.io registry
        uses: sclorg/build-and-push-action@v2
        with:
          registry: "quay.io"
          registry_namespace: "namespace"
          registry_username: ${{ secrets.REGISTRY_LOGIN }}
          registry_token: ${{ secrets.REGISTRY_TOKEN }}
          dockerfile: "Dockerfile"
          dockerfile_path: "1.0"
          suffix: "suffix"
          tag: "tag"
```
