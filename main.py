from shell import Shell

shell = Shell()

while True:
    option = input("select mode: 1.open 2.create (1/2 ?)")
    if option == "1":
        shell.open()
        break
    if option == "2":
        shell.new()
        break

shell.serve()