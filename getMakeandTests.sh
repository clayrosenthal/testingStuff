#!/bin/bash

assignment=$(pwd | rev | cut -d "/" -f 1 | rev | cut -b 1-)
echo "Getting makefile and requirements for $assignment"
cp ~kmammen-grader/evaluations/W19/357/$assignment/Makefile makefile
cp ~kmammen-grader/evaluations/W19/357/$assignment/requirements requirements

touch tests
if [ -s tests ]
then
   echo "Tests file already exists"
   make
   exit 0
fi
echo "Getting core value"
echo "Core Tests Total Value:" >> tests
cat ~kmammen-grader/evaluations/W19/357/$assignment/tests/core/value >> tests
echo "Core Tests:" >> tests
echo "Getting descriptions and values for core tests"
for coretest in $(ls ~kmammen-grader/evaluations/W19/357/$assignment/tests/core);do
   testfolder=~kmammen-grader/evaluations/W19/357/$assignment/tests/core/${coretest}
   if [ -d $testfolder ]
   then
      if [ -r $testfolder/description ]
      then
         echo ${coretest} desc: >> tests
         cat $testfolder/description >> tests
      fi
      if [ -r $testfolder/value ]
      then
         echo ${coretest} value: >> tests
         cat $testfolder/value >> tests
      fi
   fi
done

echo "Getting descriptions and values for feature tests"
echo "Feature Tests:" >> tests
for feattest in $(ls ~kmammen-grader/evaluations/W19/357/$assignment/tests/feature);do
   testfolder=~kmammen-grader/evaluations/W19/357/$assignment/tests/feature/${feattest}
   if [ -d $testfolder ]
   then
      if [ -r $testfolder/description ]
      then
         echo ${feattest} desc: >> tests
         cat $testfolder/description >> tests
      fi
      if [ -r $testfolder/value ]
      then
         echo ${feattest} value: >> tests
         cat $testfolder/value >> tests
      fi
   fi
done
