#!/bin/bash

# install dependencies locally
source /var/diagnoser/git.config

git config --global user.email "${EMAIL}"
git config --global user.name "${USERNAME}"


if [ mvn dependency:get -Dartifact=edu.ucr.cs.riple:nullaway:0.7.12-SNAPSHOT -o -DrepoUrl=file://~/.m2/repository ]; then
    :
else
    pushd /tmp/
    git clone https://${USERNAME}:${KEY}@github.com/nimakarimipour/NullAway.git
    pushd NullAway
    git checkout autofix

    ./gradlew install
    
    popd
    popd
fi

if [ mvn dependency:get -Dartifact=edu.ucr.cs.riple:annotationinjector:1.0-SNAPSHOT -o -DrepoUrl=file://~/.m2/repository ]; then
    :
else
    pushd /tmp/
    git clone https://${USERNAME}:${KEY}@github.com/nimakarimipour/AnnotationInjector.git
    pushd AnnotationInjector
    git checkout stable

    ./gradlew install
    
    popd
    popd
fi


if [ mvn dependency:get -Dartifact=edu.ucr.cs.riple:NullAwayAutoFixer:1.0-SNAPSHOT -o -DrepoUrl=file://~/.m2/repository ]; then
    :
else
    pushd /tmp/
    git clone https://${USERNAME}:${KEY}@github.com/nimakarimipour/NullAwayAutoFixer.git
    pushd NullAwayAutoFixer

    ./gradlew install

    popd
    popd
fi

pushd /tmp/
git clone https://${USERNAME}:${KEY}@github.com/nimakarimipour/Docker_AE_NA.git
pushd Docker_AE_NA
python run.py ${USERNAME} ${KEY}
popd
popd
