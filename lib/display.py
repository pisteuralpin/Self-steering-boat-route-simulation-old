def menu(options:list, question:str="Faites votre choix :"):
    """Affiche un menu et demande à l'utilisateur de faire un choix parmi les options proposées."""
    print(str(question))
    for i in range(len(options)):
        print(str(i+1) + " : " + str(options[i]))
    choice=int(input(">>> "))
    if choice <= len(options) and choice >= 0:
        print("Votre choix : " + str(options[choice-1]) + " (" + str(choice) + ")")
    return choice, options[choice-1]
