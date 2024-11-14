function calculateLoan(loanAmount, interestRate, loanTerm) {
    if (
      isNaN(loanAmount) || isNaN(interestRate) || isNaN(loanTerm) ||
      loanAmount <= 0 || interestRate <= 0 || loanTerm <= 0
    ) {
      return "Please enter valid numbers for all fields.";
    }
  
    // Convert interest rate and loan term to monthly values
    const monthlyInterestRate = interestRate / 100 / 12;
    const numberOfPayments = loanTerm * 12;
  
    // Calculate monthly payment
    const monthlyPayment = (loanAmount * monthlyInterestRate) /
      (1 - Math.pow(1 + monthlyInterestRate, -numberOfPayments));
  
    return `Estimated Monthly Payment: S$${monthlyPayment.toFixed(2)}`;
  }
  
  function testLoanCalculator() {
    const testCases = [
      {
        description: "Valid input test",
        loanAmount: 10000,
        interestRate: 5,
        loanTerm: 5,
        expected: "Estimated Monthly Payment: S$188.71"
      },
      {
        description: "Zero loan amount",
        loanAmount: 0,
        interestRate: 5,
        loanTerm: 5,
        expected: "Please enter valid numbers for all fields."
      },
      {
        description: "Zero interest rate",
        loanAmount: 10000,
        interestRate: 0,
        loanTerm: 5,
        expected: "Please enter valid numbers for all fields."
      },
      {
        description: "Zero loan term",
        loanAmount: 10000,
        interestRate: 5,
        loanTerm: 0,
        expected: "Please enter valid numbers for all fields."
      },
      {
        description: "Negative loan amount",
        loanAmount: -10000,
        interestRate: 5,
        loanTerm: 5,
        expected: "Please enter valid numbers for all fields."
      },
      {
        description: "Negative interest rate",
        loanAmount: 10000,
        interestRate: -5,
        loanTerm: 5,
        expected: "Please enter valid numbers for all fields."
      },
      {
        description: "Negative loan term",
        loanAmount: 10000,
        interestRate: 5,
        loanTerm: -5,
        expected: "Please enter valid numbers for all fields."
      }
    ];
  
    testCases.forEach(({ description, loanAmount, interestRate, loanTerm, expected }) => {
      const result = calculateLoan(loanAmount, interestRate, loanTerm);
      console.log(`${description}: ${result === expected ? "PASS" : "FAIL"} (Expected: "${expected}", Got: "${result}")`);
    });
  }
  
  testLoanCalculator();
  