class SparseMatrix:
    def load_matrix(self, file_path):
        """
        Load the sparse matrix from a file.
        The file format contains the number of rows and columns followed by non-zero values.
        Each non-zero value is stored as (row, col, value).
        """
        matrix = {}
        try:
            
            with open(file_path, 'r') as file:
                rows = int(file.readline().split('=')[1])  
                cols = int(file.readline().split('=')[1])  

                self.numRows = rows
                self.numCols = cols

                for line in file:
                    if line.strip():  
                        row, col, value = self.parse_entry(line)  
                        if row not in matrix:
                            matrix[row] = {}  
                        matrix[row][col] = value  

        except Exception as e:

            raise ValueError(f"Input file has wrong format: {e}")
        
        return matrix  

    def __init__(self, matrix_file=None, numRows=None, numCols=None):
        """
        Initialize the SparseMatrix class.
        - If `matrix_file` is provided, load the matrix from the file.
        - If `numRows` and `numCols` are provided, create an empty matrix with those dimensions.
        """
        if matrix_file:
            self.matrix = self.load_matrix(matrix_file)  
        else:
            self.matrix = {}  
            self.numRows = numRows
            self.numCols = numCols



    def parse_entry(self, line):
        """
        Parse a line containing a matrix entry.
        Each line is in the format (row, column, value).
        """

        entry = line.strip()[1:-1].split(',')
        return int(entry[0]), int(entry[1]), int(entry[2])  

    def get_element(self, row, col):
        """
        Get the value of an element at a specific row and column.
        If the element is not explicitly stored (i.e., it's zero), return 0.
        """
        return self.matrix.get(row, {}).get(col, 0) 

    def set_element(self, row, col, value):
        """
        Set a value at a specific row and column in the matrix.
        If the row or column doesn't exist, it will be initialized.
        """
        if row not in self.matrix:
            self.matrix[row] = {}  
        self.matrix[row][col] = value  

    def add(self, other_matrix):
        """
        Add this matrix to another sparse matrix.
        This operation adds non-zero elements and stores the result in a new matrix.
        """
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)  


        for row in range(self.numRows):
            for col in range(self.numCols):

                result.set_element(row, col, self.get_element(row, col) + other_matrix.get_element(row, col))
        
        return result 

    def subtract(self, other_matrix):
        """
        Subtract another sparse matrix from this matrix.
        This operation subtracts non-zero elements and stores the result in a new matrix.
        """
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)  

        
        for row in range(self.numRows):
            for col in range(self.numCols):
                
                result.set_element(row, col, self.get_element(row, col) - other_matrix.get_element(row, col))
        
        return result  

    def multiply(self, other_matrix):
        """
        Multiply this matrix with another sparse matrix.
        The operation follows matrix multiplication rules: The number of columns in the first matrix
        must be equal to the number of rows in the second matrix.
        """
        if self.numCols != other_matrix.numRows:
            raise ValueError("Matrix multiplication not possible with incompatible sizes.")  

        result = SparseMatrix(numRows=self.numRows, numCols=other_matrix.numCols)  


        for row in self.matrix:
            for col in other_matrix.matrix:
                if col in self.matrix[row]:  

                    result.set_element(row, col, sum(self.get_element(row, k) * other_matrix.get_element(k, col) 
                                                     for k in range(self.numCols)))
        
        return result  

    def save_to_file(self, file_path):
        """
        Save the sparse matrix to a file.
        The format will be similar to the input: number of rows, number of columns,
        followed by non-zero elements in (row, col, value) format.
        """
        with open(file_path, 'w') as file:
            file.write(f"rows={self.numRows}\n")
            file.write(f"cols={self.numCols}\n")
            
            for row in self.matrix:
                for col, value in self.matrix[row].items():
                    file.write(f"({row}, {col}, {value})\n")


if __name__ == "__main__":
    matrix1 = SparseMatrix(matrix_file='./easy_sample_01_3.txt')
    matrix2 = SparseMatrix(matrix_file='./easy_sample_03_1.txt')

    print("Choose a matrix operation:")
    print("1. Add Matrices")
    print("2. Subtract Matrices")
    print("3. Multiply Matrices")
    choice = int(input("Enter your choice (1/2/3): "))

    if choice == 1:
        result = matrix1.add(matrix2)
        print("Matrices added successfully!")
    elif choice == 2:
        result = matrix1.subtract(matrix2)
        print("Matrices subtracted successfully!")
    elif choice == 3:
        result = matrix1.multiply(matrix2)
        print("Matrices multiplied successfully!")
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

    output_file = input("Enter the output file path to save the result: ")
    result.save_to_file(output_file)
    print(f"Result saved to {output_file}.")
