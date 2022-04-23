#!/bin/sh
MVN=mvn
PY4J_VER_FILE=py4j_version
PY4J_VER=$(head -n1 $PY4J_VER_FILE)
JAR_DIR=${JAR_DIR:-".venv/share/py4j"}
JAR_FILE=${JAR_DIR}/py4j${PY4J_VER}.jar

$MVN install:install-file \
   -Dfile="$JAR_FILE" \
   -DgroupId=py4j \
   -DartifactId=py4j \
   -Dversion=1.0 \
   -Dpackaging=jar \
   -DgeneratePom=true
