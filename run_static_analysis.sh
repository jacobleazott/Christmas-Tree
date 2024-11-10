#!/bin/bash

echo "Running Flake8..."
flake8 .
if [ $? -ne 0 ]; then
    echo "Flake8 found issues."
fi


echo "Running Mypy..."
mypy .
if [ $? -ne 0 ]; then
    echo "Mypy found issues."
fi

echo "Running Pylint..."
pylint .
if [ $? -ne 0 ]; then
    echo "Pylint found issues."
fi


echo "All checks complete."