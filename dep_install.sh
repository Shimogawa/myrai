MVN=mvn
PY4J_VER="0.10.9.5"
JAR_FILE=".venv/share/py4j/py4j${PY4J_VER}.jar"

$MVN install:install-file \
   -Dfile=$JAR_FILE \
   -DgroupId=py4j \
   -DartifactId=py4j \
   -Dversion=1.0 \
   -Dpackaging=jar \
   -DgeneratePom=true
