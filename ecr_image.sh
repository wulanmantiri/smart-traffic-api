account=$(aws sts get-caller-identity --query Account --output text)
region=$(aws configure get region)

image_name="stms"
ecr_image_version="latest"
ecr_image_name="${account}.dkr.ecr.${region}.amazonaws.com/${image_name}:${ecr_image_version}"
echo "ECR Repo URI:" $ecr_image_name

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${image_name}" > /dev/null 2>&1
if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${image_name}" --image-scanning-configuration scanOnPush=true
fi

# Get the login command from ECR and execute it directly
aws ecr get-login-password | docker login --username AWS --password-stdin ${account}.dkr.ecr.${region}.amazonaws.com

# Modify the created Docker image from `sam build`
sam_build_image_name="detectvehicles:rapid-1.30.0"

docker tag ${sam_build_image_name} ${ecr_image_name}
docker push ${ecr_image_name}
