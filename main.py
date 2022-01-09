from table_init import TableInitializer
from batch_processor import BatchProcessor
import argparse

from dotenv import load_dotenv

def main(cutoff: int = None):
    table_init = TableInitializer()
    table_init.initialize_tables()
    table_init.close_connection()

    batch_processor = BatchProcessor()
    batch_processor.populate_queue()

    batch_processor.process_queue(cutoff=cutoff)


if __name__=="__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('cutoff', type=int, nargs='?',
                    help='Number of windows to process (until queue is empty if no input)')

    args = parser.parse_args()
    main(args.cutoff)