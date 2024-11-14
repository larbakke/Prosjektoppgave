#!/bin/bash

# This script is used to initialize the IDUN environment
echo "Initializing IDUN environment..."

module purge
echo "purged modules"

echo "loading modules..."
module load Anaconda3/2024.02-1
module load nodejs/18.17.1-GCCcore-12.3.0

echo "IDUN environment initialized."