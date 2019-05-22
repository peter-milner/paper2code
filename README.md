# paper2code

*Warning
Use at your own risk. paper2code uses [Restricted Python](https://restrictedpython.readthedocs.io/en/latest/index.html) to define a subset of Python that is allowed to be executed. However, there could still be potential vulnerabilities.

### Prep
1. Obtain Google Application Key and download to a local path
2. Rename file to `p2p.json`
2. Export path with keys (needs to be done every shell session, consider adding to `~/.bashrc`): `export GOOGLE_APPLICATION_CREDENTIALS="path/to/p2p.json"`

### Building and testing using Google Cloud Run
- Build: `gcloud builds submit --tag gcr.io/[PROJECT-ID]/[IMAGE]`
- Local testing: 
```
PORT=8080 && docker run -p 8080:${PORT} \
--name my-p2p \
-e PORT=${PORT} \
-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/p2p.json \
-v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/p2p.json:ro \
-v </path/to/src>:/app \
gcr.io/[PROJECT-ID]/[IMAGE]
```

### Add package
1. Have container up and running
2. Access docker container shell: `docker exec -it my-p2p sh`
3. Exit app folder `cd ..`
3. Install package: `pipenv install <package-name>` *Note use --dev for dev packages
4. Copy Pipfile and Pipfile.lock to local directory: `docker cp my-p2p:/Pipfile . && docker cp my-p2p:/Pipfile.lock .`

### Linting
`docker exec -it my-p2p pipenv run pylint app`
- Add lint pre-commit hook: `cp pre-commit.sh .git/hooks/pre-commit`. Can also use a symlink here

### Deployment to Google Cloud Run
1. Ensure you are using `Dockerfile.prod`
2. Generate requirements.txt using pipenv (need to do this within local container): `pipenv lock -r > requirements.txt`
2. Deploy: `gcloud builds submit --tag gcr.io/[PROJECT-ID]/[IMAGE]`
3. Ensure Cloud Run service is selected to newest image.