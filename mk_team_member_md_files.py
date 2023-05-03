#!/usr/bin/python3
"""
Convert a table with 1+ team member information into team markdown files (1 per team member)
"""
import sys
import os
import re
import argparse

def main():

    args = _parse_cmd_line()

    with open(args.file, 'r') as fh:
        for line in fh:
            if (line.startswith('first\t')):
                continue
            line = line.rstrip('\n')
            cols = line.split('\t')
            first_name = cols[0]
            last_name = cols[1]
            importance = cols[2]
            title = cols[3]
            short_bio = cols[4]
            email = cols[5]
            long_bio = cols[6]
            category = cols[7]

            _make_team_member_file(first_name, last_name, importance, title, email, category, short_bio, long_bio, args)

    return(0)

def _sanitize_for_fn(var):
    # lowercase
    var = var.lower()

    # Replace any non alphanumeric/-/_/ for '_'
    var = re.sub('[^a-z0-9_]', '_', var)      

    # Replace 2+ '_' for just 1 '_'
    var = re.sub('_+', '_', var)

    # Replace '_$' and '^_' for ''
    var = re.sub('_$', '', var)
    var = re.sub('^_', '', var)

    return(var)

def _write_new_file_message(fn):
    messsage = "created %s" % fn
    _write_info_message(messsage)
    return(0)

def _write_info_message(message):
    print("INFO: %s" % (message), file=sys.stderr)

def _make_team_member_file(first_name, last_name, importance, degree, email, category, short_bio, long_bio, args):

    sanitized_name = _sanitize_for_fn(' '.join([first_name, last_name]))

    # Create YAML key:value pairs
    yaml_data = {}
    yaml_data['layout'] = 'person'
    yaml_data['title'] = '%s %s' % (first_name, last_name)
    if (degree != ''):
        yaml_data['title'] = '%s, %s' % (yaml_data['title'], degree)
    yaml_data['email'] = email

    if (short_bio == ''):
        short_bio = _long_bio2short_bio(long_bio)

    yaml_data['description'] = short_bio

    # Image
    yaml_data['img'] = 'assets/img/%s.jpg' % (sanitized_name)
    real_img_fn = os.path.exists(os.path.join(args.local_base_path, yaml_data['img']))
    if (not os.path.exists(real_img_fn)):
        _write_warning_message('image file %s does not exist' % (real_img_fn))

    yaml_data['category'] = category

    yaml_data['bio_long'] = '|\n %s'% (long_bio) # IMPORTANT: space at beginning of line is needed for correct parsing

    yaml_data['importance'] = importance

    team_member_fn = '%s.md' % (sanitized_name)
    # Check if it exists

    if (os.path.exists(team_member_fn) and (not args.force)):
        _write_error_message('team member output file %s already exists and you didn\'t want to overwrite it.  Delete it or use --force' % (team_member_fn))
        exit(1)

    with open(team_member_fn, 'w') as team_member_fh:
        key_order = ['layout', 'title', 'email', 'description', 'img', 'importance', 'category', 'bio_long']

        # Print YAML
        print("---", file=team_member_fh)
        for k in key_order:
            print("%s: %s" % (k, yaml_data[k]), file=team_member_fh)
        print("---", file=team_member_fh)

        # Print markdown/html
        # None at this time

    _write_new_file_message(team_member_fn)

def _write_error_message(message):
    print("ERROR: %s" % (message), file=sys.stderr)


def _write_warning_message(message):
    print("WARNING: %s" % (message), file=sys.stderr)

def _long_bio2short_bio(biography):
    
    # Grab the first 200 characters but split nicely on words
    bio_length = 200

    if (len(biography) <= bio_length):
        short_bio = biography
    else:
        short_bio = biography[0:bio_length]
    
        # If in the middle of the word, chew off the word
        # There's probably a more efficient way to do this
        if short_bio[bio_length - 1] != ' ':
           tmp = short_bio.split(' ') 
           short_bio = ' '.join(tmp[0:(len(tmp) - 1)])

           short_bio += ' ...'

    return short_bio



def _email2munged_email(email):

    x = email.split("@")
    name = x[0]
    domain = x[1]
    domain_index = 3
    if (len(domain) < domain_index):
        print("Email domain too short for current munging strategy.  Update strategy.", file=sys.stderr)

    munged_email = '<p><span style="color:#215990;">%s<span class="munge">xxx</span>&#x40;%s<span class="munge">xxx</span>%s</span></p>' % (name, domain[0:domain_index], domain[domain_index:len(domain)])

    return munged_email


def _parse_cmd_line():
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
        pass

    parser = argparse.ArgumentParser(
        formatter_class=CustomFormatter,
        description=__doc__,
    )

    parser.add_argument(
        '--file',
        '-f',
        required=True,
        help='Path to file containing team member information.  Format: tsv.  Requred columns: name; short_bio; email; long_bio; category.  (Elements can be blank for a given team member)'
    )

    parser.add_argument(
        '--local-base-path',
        '-l',
        required=True,
        help='Path to local base.  Used to make sure image files exist.'
    )

    parser.add_argument(
        '--force',
        '-r',
        required=False,
        default=False,
        action='store_true',
        help='If specified, output files (if they exist) will be overwritten.'
    )


    args = parser.parse_args()

    return(args)

if __name__ == '__main__':
    main()

