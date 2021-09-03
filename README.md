# Smart Traffic Management System API

## Getting Started

1. Install [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).
2. Clone the repository and enter the project directory with `cd smart-traffic-api`.
3. Build the dependencies with `sam build`.
4. Run the api with `sam local start-api -p 8000`.
5. Open [localhost:8000](http://localhost:8000) in apps like Postman.

To learn AWS SAM, check out the [AWS SAM documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html).

## Deployment: CI/CD with AWS

### S3
- Create an S3 bucket with the default configurations.

### CodeBuild
- Create a build project and connect to github repository. 
- Enable webhook to rebuild as code changes and add `PUSH` event types.
- Select `Managed image` as environment image with `Amazon Linux 2` OS and `x86_64:3.0` image. Use or create new service role that allows access to your S3 bucket and CloudFormation.
- In `additional configuration`, add `SAM_S3_BUCKET_NAME`, `CLOUDFORMATION_STACK_NAME` and `REGION` values in environment variables. Optionally, set compute to the lowest spec.
- Leave everything as is for easy configuration.

After setup, every push to `master` will trigger CI/CD.
