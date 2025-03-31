from window import Window


def main() -> None:
    win: Window = Window(800, 600)
    win.wait_for_close()


if __name__ == "__main__":
    _ = main()
