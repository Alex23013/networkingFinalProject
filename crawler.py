import re
import sys
import subprocess


def run_command(arg_list):
    result = subprocess.run(arg_list, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


def extract_text_links(url):
    '''
    Returns the text and a links of links of the url's web page.
    '''
    arg_list = ['lynx', '-dump', '-nonumbers',
                '-accept_all_cookies',
                '-assume_charset=utf-8',
                '-assume_unrec_charset=UTF-8',
                '-display_charset=utf-8',
                url]

    text = ''
    links = []
    try:
        all = run_command(arg_list)

        idx_links = all.rfind("Visible links:")
        idx_hidden_links = all.rfind("Hidden links:")

        text = all[:idx_links]
        links_str = all[idx_links:idx_hidden_links]

        if (links_str):
            new_line_idx = links_str.find('\n')
            links_str = links_str[new_line_idx:].strip()
            links = list(dict.fromkeys(links_str.splitlines()))
    except:
        print("++ ", url)
        pass
    return text, links


def extract_content_type(url):
    pattern = re.compile(r'Content-Type: (\w+)/(\w+)')
    arg_list = ['lynx', '-dump', '-head', url]

    header = run_command(arg_list)
    match = pattern.search(header)
    if not match:
        return "undefined"

    return match[2][:4]  # Type id must  be 4 chars long.


if __name__ == '__main__':
    #text, links = extract_text_links(sys.argv[1])
    type_ = extract_content_type(sys.argv[1])
    print(type_)
