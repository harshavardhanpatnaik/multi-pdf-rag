from rag.rag_pipeline import RAG
import os
from src.database.database import (
    create_tables,
    get_connection,
    insert_pdf,
    check_pdf,
    show,
)

# Create database tables
create_tables()

rag = RAG()


def main():

    while True:

        print("\n1. upload pdf ")
        print("2. use existing pdf")
        print("3. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            path = input("Enter PDF Path without quoates : ").strip()

            if not os.path.exists(path):
                print("PDF not exists")
                continue

            data = check_pdf(path)

            if data:
                print("PDF already exists")

                document_id = data[0]
                embedded = data[3]

                if embedded == 1:
                    print("Already stored in vector db ")

                    rag.use_exisiting_pdf(document_id)
                else:

                    rag.ingest_pdf(path, document_id)

            else:
                document_id = insert_pdf(path)
                rag.ingest_pdf(path, document_id)

            continution()

        elif choice == 2:
            data = show()
            if not data:
                print("No existing pdf found ")
                continue

            for i, document in enumerate(data, start=1):
                value = document[1]
                print(f"{i}. {value} ")

            chc = int(input("Enter your choice : "))
            if chc < 1 or chc > len(data):
                print("Invalid choice : ")
                continue

            dattt = data[chc - 1]
            document_id = dattt[0]

            rag.use_exisiting_pdf(document_id)
            continution()

        elif choice == 3:
            print("Exiting.....")
            break
        else:
            print("Invalid choice")


def continution():
    while True:
        print("\n 1.Ask Question ")
        print("2. Exit")

        choice = int(input("Enter your choice : "))

        if choice == 1:
            question = input("Enter Your qustion : ")
            rag.ask(question)
            print("==*20")
            print(rag.answer)

        elif choice == 2:
            print("Exiting........")
            break

        else:
            print("Invalid choice ")


if __name__ == "__main__":
    main()
