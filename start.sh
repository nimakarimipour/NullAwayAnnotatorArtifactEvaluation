#!/bin/bash

# install dependencies locally


# if [ mvn dependency:get -Dartifact=edu.ucr.cs.riple:nullaway:0.7.12-SNAPSHOT -o -DrepoUrl=file://~/.m2/repository]; then
#     :
# else
#     pushd /tmp/
#     git clone git@github.com:nimakarimipour/NullAway.git
#     pushd NullAway
#     git checkout autofix

#     ./gradlew install
    
#     popd
#     popd
# fi

# if [ mvn dependency:get -Dartifact=edu.ucr.cs.riple:AnnotationInjector:1.0-SNAPSHOT -o -DrepoUrl=file://~/.m2/repository]; then
#     :
# else
#     pushd /tmp/
#     git clone git@github.com:nimakarimipour/AnnotationInjector.git
#     pushd AnnotationInjector

#     ./gradlew install
    
#     popd
#     popd
# fi


# if [ mvn dependency:get -Dartifact=edu.ucr.cs.riple:NullAwayAutoFixer:1.0-SNAPSHOT -o -DrepoUrl=file://~/.m2/repository]; then
#     :
# else
#     pushd /tmp/
#     git clone git@github.com:nimakarimipour/NullAwayAutoFixer.git
#     pushd NullAwayAutoFixer

#     ./gradlew install

#     popd
#     popd
# fi

source git.config
echo "https://${USERNAME}:${KEY}@github.com/nimakarimipour/Docker-AE-NAF.git"



# export username="nimakarimipour"
# export key="d829ba81308d1c67d1899208153682ddbb1c4ebf"
# export key=`cat git.key`
# export email="karimipour.nima@gmail.com"

# echo "${key}"
# mkdir repo
# cd repo
# git init
# git config user.email "${email}"
# git config user.name "${username}"
# echo "https://${username}:${key}@github.com/nimakarimipour/Docker-AE-NAF.git"
# git clone https://${username}:${key}@github.com/nimakarimipour/Docker-AE-NAF.git