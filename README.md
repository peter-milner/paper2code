# paper2code

### Prep
1. Obtain Google Application Key and download to a local path
2. Export the path (needs to be done every shell session, perhaps add to `~/.bashrc`): `export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"`

### Building and testing using Google Cloud
- Build: `gcloud builds submit --tag gcr.io/[PROJECT-ID]/[IMAGE]`
- Local testing: `PORT=8080 && docker run -p 8080:${PORT} -e PORT=${PORT} -v <local location of src folder>:/app --name my-p2p gcr.io/[PROJECT-ID]/[IMAGE]`

### Add package
1. Have container up and running
2. Access docker container shell: `docker exec -it my-p2p sh`
3. Install package: `pipenv install <package-name>` *Note use --dev for dev packages
4. Copy Pipfile and Pipfile.lock to local directory: `docker cp my-p2p:/app/Pipfile . && docker cp my-p2p:/app/Pipfile.lock .`

### Linting
`docker exec -it my-p2p pipenv run pylint app`
- Add lint pre-commit hook: `cp pre-commit.sh .git/hooks/pre-commit`. Can also use a symlink here.