import inquirer

def checbox(options=['deafult'], message='Choose stack', name='stack'):
    questions = [
    inquirer.Checkbox(name, message=message, choices=options),    
    ]

    answers = inquirer.prompt(questions)

    return answers

def get_input(questions=[('name', 'message')]):
    questions_list = [inquirer.Text(name, message=message) for name, message in questions] 
    answers = inquirer.prompt(questions_list)
    return answers






