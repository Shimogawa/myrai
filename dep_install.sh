MVN=mvn
PY4J_VER="0.10.9.5"
JAR_DIR=${JAR_DIR:-".venv/share/py4j"}
JAR_FILE=${JAR_DIR}/py4j${PY4J_VER}.jar

$MVN install:install-file \
   -Dfile=$JAR_FILE \
   -DgroupId=py4j \
   -DartifactId=py4j \
   -Dversion=1.0 \
   -Dpackaging=jar \
   -DgeneratePom=true
