import sys

from Scanner import Scanner

class Lox:
    hadError = False

    def run(self, string):
        if self.hadError:
            sys.exit(0)

        scanner = Scanner(string)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token)


    def runFile(self, path):
        f = open(path, 'r')
        self.run(f.read())
    
    def runPrompt(self):
        print('> ')
        for line in sys.stdin:
            self.run(line)
            self.hadError = False

    def main(self):
        args_length = len(sys.argv)
        if args_length > 2:
            print('Usage: plox [script]')
        elif args_length == 2:
            self.runFile(sys.argv[1])
        else:
            self.runPrompt()


    def error(self, line, message):
        self.report(line, '', message)

    def report(self, line, where, message):
        print('[line {}] Error{}: {}'.format(line, where, message))
        self.hadError = True




if __name__ == '__main__':
    Lox().main()