import subprocess


class gnuplot:
    def __init__(self, gnu_path):
        self.proc = subprocess.Popen(
            [gnu_path.replace("\\", "/"), "-p"],
            shell=True,
            stdin=subprocess.PIPE,
        )
        self.command = ""
        self.plot_count = 0

    def quit(self):
        self.proc.kill()

    def run_command(self, command):
        self.proc.stdin.write((command + "\n").encode("ascii"))

    def set_label(self, xlabel, ylabel):
        self.proc.stdin.write(f'set xlabel "{xlabel}"\n'.encode("ascii"))
        self.proc.stdin.write(f'set ylabel "{ylabel}"\n'.encode("ascii"))

    def set_title(self, title):
        self.proc.stdin.write(f'set title "{title}" noenhanced\n'.encode("ascii"))

    def draw(self):
        self.proc.stdin.write("set nokey\n".encode("ascii"))
        self.proc.stdin.write("replot\n".encode("ascii"))
        self.proc.stdin.write(
            "pause mouse close\n".encode("ascii")
        )  # hold the gnuplot window
        self.proc.stdin.write("quit\n".encode("ascii"))  # close the gnuplot window
        self.proc.stdin.flush()
