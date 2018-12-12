import slave_proc as slave

class CommandLineInterface(object):
    def input_command(self, command):
        tokens = self.parse_command(command=command)
        self.process_tokens(tokens=tokens)

    def parse_command(self, command):
        return str(command).split()

    def process_tokens(self, tokens):
        if tokens[0] == "process":
            self.crawl_first_url(tokens[1])

        elif tokens[0] == "stop":
            self.cancel_process()

        elif tokens[0] == "search":
            self.search_for()

    def crawl_first_url(self, url):
        """Send the url to the crawler"""
        pass

    def cancel_process(self):
        """Cancell the crawling process"""
        pass

    def search_for(self):
        """TODO Search for something i dont remember"""
        pass

