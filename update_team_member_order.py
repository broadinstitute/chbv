#!/usr/bin/python3
"""
Given a category of team members, e.g., data generation, update the importance field so that the team members are listed in alphabetical order.
"""
import sys
import os
import re
import argparse
import subprocess
import fileinput
import shlex
def main():

    args = _parse_cmd_line()

    # Find all the team member files for the given category
    team_fns = _get_team_member_files(args)

    # Determine sorted order
    team_fns = _sort_team_fns(team_fns)

    # Update importance field
    _update_team_member_importance(team_fns)

def _sort_team_fns(team_fns):
    # files are <path>/<first>_<last>.md

    name2path = {}
    for team_fn in team_fns:
        bn_sans_ext = os.path.splitext(os.path.basename(team_fn))[0]
        tmp = bn_sans_ext.split('_')
        if (len(tmp) != 2):
            print(sprintf("ERROR: did not parse name correctly in file %s" % team_fn), file=sys.stderr())
        name = '%s %s' % (tmp[1], tmp[0]) # Include first in case there are ties

        name2path[name] = team_fn

    # Sort by last name, then first name
    sorted_team_fns = [name2path[name] for name in sorted(name2path.keys())]

    return(sorted_team_fns)

def _update_team_member_importance(team_fns):
    # Update team member importance and print a summary of changes

    for i in range(len(team_fns)):
        team_fn = team_fns[i]
        new_importance = i + 1 # 1-based
        found = 0
        for line in  fileinput.input(team_fn, inplace=True):
            m = re.search('^importance: (\d+)$', line)
            if not (m is None): 
                old_importance = int(m.group(1))
                found = 1
                line = "importance: %d" % (new_importance)
                print('INFO: %s updated %d --> %d' % (team_fn, old_importance, new_importance), file=sys.stderr)
            print(line) # Will print to input file inplace


    return 0

def _get_team_member_files(args):

    # Find all team member files and filter for just the category of interest

    cmd = "grep --files-with-matches \"^category: %s\" %s" % (args.category, os.path.join(args.team_directory, '*md'))
    #cmd = ["grep", "--files-with-matches", "\"^category: %s\"" % (args.category), os.path.join(args.team_directory, '*md')]
    print(cmd)

    with subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) as p:
        p.wait()
        team_fns = p.stdout.read().decode("utf-8")
        return_code = p.returncode
    if return_code:
        sys.exit('ERROR: command \'%s\' had a nonzero exit status (%d).\n\n' % (' '.join(cmd), return_code))

    team_fns = team_fns.rstrip()
    team_fns = team_fns.split('\n')
    return(team_fns)


def _parse_cmd_line():
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
        pass

    parser = argparse.ArgumentParser(
        formatter_class=CustomFormatter,
        description=__doc__,
    )

    parser.add_argument(
        '--category',
        '-c',
        required=True,
        choices=['Computational Analysis', 'Data Generation', 'Project Management and Operations', 'Co-investigators'],
        help='Category of team members to alphabetize.'
    )

    parser.add_argument(
        '--team-directory',
        '-t',
        required=True,
        help='Path to team directory, e.g. chbv/_team.'
    )


    args = parser.parse_args()

    return(args)

if __name__ == '__main__':
    main()

