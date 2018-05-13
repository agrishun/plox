import sys
import textwrap

class GenerateAst():
    def main(self, args):
        if len(args) != 1:
            print("Usage: generate_ast <output directory>")
            sys.exit(1)
        output_dir = args[0]
        self.define_ast(output_dir, "Expr", [
            "Binary   : left, operator, right",
            "Grouping : expression",
            "Literal  : value",
            "Unary    : operator, right"
        ])

    def define_ast(self, output_dir, base_name, types):
        path = f'{output_dir}/{base_name.lower()}.py'
        with open(path, "w") as writer:
            writer.write('from abc import ABC, abstractmethod\n')
            writer.write(f'class Interface(ABC):\n')
            self.defineVisitor(writer, base_name, types)
            for expression_type in types:
                class_name = expression_type.split(':')[0].strip()
                fields = expression_type.split(':')[1].strip()
                self.define_type(writer, base_name, class_name, fields)
            writer.close()

    def define_type(self, writer, base_name, class_name, fields_list):
        writer.write(f'class {class_name}():\n')
        writer.write(textwrap.indent(f'def __init__(self, {fields_list}):\n', '\t'))
        fields = fields_list.split(', ')
        for field in fields:
            writer.write(textwrap.indent(f'self.{field} = {field}\n', '\t\t'))
        writer.write(textwrap.indent(f'def accept(self, visitor):\n', '\t'))
        writer.write(textwrap.indent(f'return visitor.visit{class_name}{base_name}(self)\n', '\t\t'))
        writer.write('\n')

    def defineVisitor(self, writer, base_name, types):
        for expression_type in types:
            type_name = expression_type.split(':')[0].strip()
            writer.write(textwrap.indent(f'@abstractmethod\n', '\t'))
            writer.write(textwrap.indent(f'def visit{type_name}{base_name}(self, {base_name.lower()}): raise NotImplementedError\n\n', '\t'))

if __name__ == '__main__':
    GenerateAst().main(sys.argv[1:])