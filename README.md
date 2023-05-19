# The Build and Push GitHub Action

The action builds a container image and pushes it to the specified registry.
The path to upload the image is constructed from inputs as follows:
```
registry/registry_namespace/image_name
```

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
| `image_name` | Name of the built image. | **required** |
| `tag` | Tag of the built image. | "" |
| `archs` | Label the image with this architecture. For multiple architectures, seperate them by a comma. | amd64 |
| `dockerfile` | Dockerfile and its relative path to build the image. | Dockerfile |
| `docker_context` | Docker build context. | . |



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
          dockerfile: "1.20/Dockerfile"
          image_name: "container_image-1.20"
          tag: "tag"
```

## Multi arch builds
Input `archs` is provided to build the multi architecture images. `archs` input should be comma separated ( i.e. `archs: "amd64, s390x"` ). It is an optional argument, if not provided image will be built on amd64 i.e. default arch

The example below shows how the `sclorg/build-and-push-action` can be used for multi-arch image 

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
          dockerfile: "1.20/Dockerfile"
          image_name: "container_image-1.20"
          tag: "tag"
          archs: "amd64, s390x"
```

