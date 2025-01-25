import sys


def get_clients():
    clients = [
        "andrew@gmail.com",
        "jessica@gmail.com",
        "ted@mosby.com",
        "john@snow.is",
        "bill\_gates@live.com",
        "mark@facebook.com",
        "elon@paypal.com",
        "jessica@gmail.com",
    ]
    return clients


def get_participants():
    participants = [
        "walter@heisenberg.com",
        "vasily@mail.ru",
        "pinkman@yo.org",
        "jessica@gmail.com",
        "elon@paypal.com",
        "pinkman@yo.org",
        "mr@robot.gov",
        "eleven@yahoo.com",
    ]
    return participants


def get_recipients():
    recipients = ["andrew@gmail.com", "jessica@gmail.com", "john@snow.is"]
    return recipients


def call_center(clients, recipients):
    return list(set(clients).difference(recipients))


def potential_clients(clients, participants):
    return list(set(participants).difference(clients))


def loly_program(clients, participants):
    return list(set(clients).difference(participants))


def main():
    try:
        if len(sys.argv) == 2:
            task = sys.argv[1]
            if task == "call_center":  # кто не видел рекламное письмо
                clients = get_clients()
                recipients = get_recipients()
                call_list = call_center(clients, recipients)
                print(call_list)
            elif task == "potential_clients":  # посетили мероприятие, но не клиенты
                clients = get_clients()
                participants = get_participants()
                potential_list = potential_clients(clients, participants)
                print(potential_list)
            elif task == "loly_program":
                clients = get_clients()
                participants = get_participants()
                loly_list = loly_program(
                    clients, participants
                )  # клиенты, не посетили мероприятие
                print(loly_list)
            else:
                raise Exception("Incorrect task in argument")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
