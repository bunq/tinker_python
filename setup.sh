#!/usr/bin/env bash

# Error constants.
ERROR_SYSTEM_UNKNOWN='Unknown system found "%s".\n'
ERROR_RUN_IN_EMPTY_DIRECTORY='Please run the script from an empty directory\n'
ERROR_COULD_NOT_FIND_COMMAND='Could not find "%s", try installing it by running "%s".'

# System Constants
SYSTEM_NAME_LINUX='Linux'
SYSTEM_NAME_MAC_OS='Darwin'
SYSTEM_NAME_FREEBSD='FreeBSD'
ALL_SYSTEM_SUPPORTED="${SYSTEM_NAME_LINUX} ${SYSTEM_NAME_MAC_OS} ${SYSTEM_NAME_FREEBSD}"

# Prerequisite constants.
PREREQUISITE_CONSTANT_PREFIX='ALL_PREREQUISITE_'
ALL_PREREQUISITE_GLOBAL='git python3 pip pipenv qrencode jq'
ALL_PREREQUISITE_LINUX=''
ALL_PREREQUISITE_DARWIN='brew'
ALL_PREREQUISITE_FREEBSD=''

# Installation method constants.
COMMAND_INSTALLATION_PREFIX='COMMAND_INSTALLATION_'
COMMAND_INSTALLATION_LINUX='apt-get install'
COMMAND_INSTALLATION_DARWIN='brew install'
COMMAND_INSTALLATION_FREEBSD='pkg install'

# Version index
INDEX_VERSION_MAJOR='0'
INDEX_VERSION_MINOR='1'
INDEX_VERSION_PATCH='2'

# Platform specific sed command
COMMAND_SED_PREFIX='COMMAND_SED_'
COMMAND_SED_LINUX='sed -rn'
COMMAND_SED_DARWIN='sed -En'
COMMAND_SED_FREEBSD='sed -rn'

function assertIsSystemSupported
{
  contains "${ALL_SYSTEM_SUPPORTED}" "$(determineSystemName)" \
    && return 0 || printf "${ERROR_SYSTEM_UNKNOWN}" "$(determineSystemName)" >&2 && exit 1
}

function assertIsRanInEmptyDirectory
{
    [ "$(ls -1A | wc -l)" -eq 0 ] && return 0 || printf "${ERROR_RUN_IN_EMPTY_DIRECTORY}" >&2 && exit 1
}

function assertAllPrerequisitePresent
{
    allPrerequisiteMissing="$(determineAllPrerequisiteMissing)"

    if [ -z "${allPrerequisiteMissing}" ]; then
        # All prerequisites are available
        return 0
    else
        echo -n "$(determineInstructionInstallationAllPrerequisiteMissing "${allPrerequisiteMissing}")"

        exit 1
    fi
}

function determineAllPrerequisiteMissing
{
  for prerequisite in $(determineAllPrerequisite); do
    which "${prerequisite}" > /dev/null || echo "${prerequisite}"
  done
}

function determineAllPrerequisite
{
    echo "$(determineAllPrerequisiteSystemSpecific) ${ALL_PREREQUISITE_GLOBAL}"
}

function determineAllPrerequisiteSystemSpecific
{
  prerequisiteConstantName="${PREREQUISITE_CONSTANT_PREFIX}$(capitalize $(determineSystemName))"
  echo "${!prerequisiteConstantName}"
}

function determineInstructionInstallationAllPrerequisiteMissing
{
    allPrerequisiteMissing="${1}"
    systemName="$(determineSystemName)"

    for prerequisiteMissing in ${1}; do
        prerequisiteMissingCapitalized="$(capitalizeFirstLetter ${prerequisiteMissing})"

        if declare -F "determineInstructionInstallation${prerequisiteMissingCapitalized}${systemName}" > /dev/null ; then
            echo "$(determineInstructionInstallation${prerequisiteMissingCapitalized}${systemName})" >&2
        elif declare -F "determineInstructionInstallation${prerequisiteMissingCapitalized}" > /dev/null ; then
            echo "$(determineInstructionInstallation${prerequisiteMissingCapitalized})" >&2
        else
            echo "$(determineInstructionInstallation "${prerequisiteMissing}" "${systemName}")" >&2
        fi
    done
}

function determineInstructionInstallationBrewDarwin
{
    echo -ne "Could not find \"brew\", install this by running: \033[1m/usr/bin/ruby -e \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)\"\033[0m"
    echo ", or checkout how to install this by going to https://brew.sh."
}

function determineInstructionInstallationPip
{
    printf 'Could not find "pip", try installing it by running "easy_install pip".'
}

function determineInstructionInstallationPipenv
{
    printf 'Could not find "pipenv", try installing it by running "pip install pipenv".'
}

function determineInstructionInstallationQrencodeFreeBSD
{
    determineInstructionInstallation "qrencode" "$(determineSystemName)" "libqrencode"
}

function determineInstructionInstallation
{
    programName="${1}"
    systemName="${2}"
    programPackageName=${3:-${programName}}
    commandInstallationConstantName="${COMMAND_INSTALLATION_PREFIX}$(capitalize ${systemName})"
    printf "${ERROR_COULD_NOT_FIND_COMMAND}" "${programName}" "${!commandInstallationConstantName} ${programPackageName}"
}

function determineSystemName
{
    echo "$(uname -s)"
}

function determineSedCommand
{
  commandSedConstantName="${COMMAND_SED_PREFIX}$(capitalize $(determineSystemName))"
  echo "${!commandSedConstantName}"
}

function cloneTinkerPython
{
    git clone https://github.com/bunq/tinker_python.git .
    git checkout master
}

function pipenvInstall
{
    PIPENV_VENV_IN_PROJECT=1 pipenv install
}

function startTinker
{
    ./go-tinker
}

function contains
{
    [[ ${1} =~ (^|[[:space:]])${2}($|[[:space:]]) ]] && return 0 || return 1
}

function capitalize
{
    echo "${@}" | tr [:lower:] [:upper:]
}

function capitalizeFirstLetter
{
    echo "$(capitalize ${1:0:1})${1:1}"
}

assertIsSystemSupported
assertIsRanInEmptyDirectory
assertAllPrerequisitePresent
cloneTinkerPython
pipenvInstall
startTinker

exit 0
