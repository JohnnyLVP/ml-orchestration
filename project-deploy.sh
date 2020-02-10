#!/usr/bin/env bash
run_steps(){
  wrk_space_bucket="${org_prefix}-bigdata-models-dlk-${app_env}"

  buckets_list=( $wrk_space_bucket )

  for bucket in "${buckets_list[@]}"
  do
    printf "checking... $bucket\n"
    if aws s3 ls "s3://$bucket" 2>&1 | grep -q 'NoSuchBucket'; then
      printf "creating $bucket\n"
      aws s3 mb s3://$bucket --region $region
    fi
  done

  timestamp=$(date +%s)
  tmp_dir_parent="/tmp/mlo/uploads/main/$timestamp"

  tmp_deploy=$tmp_dir_parent/deploy
  tmp_setup=$tmp_dir_parent/setup

  mkdir -p $tmp_deploy
  mkdir -p $tmp_setup

  cd lambdas

  zip_lambda () {
    fname=$(ls $1 | xargs -n 1 basename | cut -d '.' -f1)
    zip -r "$tmp_deploy/$fname.zip" $1 constants/ utils/
  }

  arr_lambdas=($(ls -d *.py))
  ## zipping and uploading lambdas to wrk_space_bucket/deployment_tag/
  for lambda_file in "${arr_lambdas[@]}"; do
    zip_lambda $lambda_file
  done

  cd ..

  arr_template_files=($(ls -d cloudformation/deploy/*))
  for template_file in "${arr_template_files[@]}"; do
    cp $template_file $tmp_deploy/.
  done

  cp algorithm_list.json $tmp_deploy

  arr_setup_files=($(ls -d cloudformation/setup/*))
  for setup_file in "${arr_setup_files[@]}"; do
    mv $setup_file $tmp_setup/
  done

  aws s3 sync $tmp_dir_parent s3://$wrk_space_bucket/template-uploads/
  rm -rf $tmp_dir_parent
}

print_usage_and_exit(){
  printf "\nArguments are:\n"

  # mandatory parameters
  printf "\t1. App Envrionment (lowercase only, ex: dev, qas, prd)\n"

  # optional parameters
  printf "\t3. Region (optional, lowercase only, default is us-east-1)\n"
  printf "\t4. Organisation Prefix (optional, lowercase only, default is belc)\n"

  exit
}

if [ $# -lt 2 ]
then
  print_usage_and_exit
fi


region="us-east-1"
org_prefix="belc"

app_env=$1

if [ $# = 3 ]; then
  echo "Region is set to $3"
  region=$3
fi

if [ $# = 4 ]; then
  echo "Region is set to $3"
  region=$3
  echo "Org prefix is set to $4"
  org_prefix=$4
fi

if [ $region != 'us-east-1' ] && [ $region != 'us-west-2' ]; then
  printf "Unexpected Region argument value"
  print_usage_and_exit
fi

if [ $org_prefix != 'belc' ]; then
  printf "Unexpected Organisation Prefix argument value"
  print_usage_and_exit
fi

run_steps