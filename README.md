# Smart Traffic Management System (STMS) API

## Getting Started

1. Install and configure [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html), [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html), and [Docker](https://docs.docker.com/get-docker/).
2. Clone the repository and enter the project directory with `cd smart-traffic-api`.
3. Run Docker and build the dependencies with `sam build --cached --parallel`.
4. Run the api with `sam local start-api -p 8000`.
5. Open [localhost:8000](http://localhost:8000) in apps like Postman.

To learn AWS SAM, check out the [AWS SAM documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html).

## Deployment: CI/CD with AWS

### Instructions
- You will need an AWS account.
- Modify the variables in `build.sh`.
- Run `chmod 755 build.sh` and `./build.sh`. Copy the ECR Repo URI. This will push SAM local image to ECR manually (might take some time).
- Setup AWS services by following the guidelines below.
- After setup, every push to `master` in your github repository will trigger CI/CD.

### S3
- Create two S3 buckets with the name `smart-traffic-sam-<RANDOM-ID>` and `smart-traffic-firehose-<RANDOM-ID>`.
- Leave everything as is for easy configuration.

### Kinesis Firehose
- Create a new delivery stream.
- Set source to be `Direct PUT` and select `Amazon S3` as the destination.
- Set the name to be `smart-traffic-stream`.
- Choose `smart-traffic-firehose` in the S3 bucket destination settings.
- Leave everything as is for easy configuration.

### CodeBuild
- Create a build project with the name `smart-traffic-api-build` and connect to your github repository.
- Enable webhook to rebuild as code changes and add `PUSH` event types.
- Select `Managed image` as environment image with `Amazon Linux 2` OS and `x86_64:3.0` image.
- Use or create new service role that allows full access to your S3 bucket, CloudFormation, Lambda, API Gateway, and IAM access.
- In `additional configuration`, add the following environment variables:
    1. key: `SAM_S3_BUCKET_NAME`, value: `smart-traffic-sam-<RANDOM-ID>`
    2. key: `CLOUDFORMATION_STACK_NAME`, value: `stms-api`
    3. key: `ECR_REPO_URI`, value: `<ECR-Repo-URI from build.sh>`
- Optionally, set compute to the lowest spec.
- Leave everything as is for easy configuration.

### Quicksight

- Sign up with Standard account. Select your desired region.
- In `Datasets`, create new dataset. Select S3 as the data source.
- Set your data source name and upload manifest file from `quicksight/manifest.json`.
- Choose `Connect`, then Visualize. You may have to give Amazon QuickSight explicit permissions to your S3 bucket.
