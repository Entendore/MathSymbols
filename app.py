import sys
import random
import csv
import json
import html
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, 
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QHeaderView, QLabel, QLineEdit, QPushButton, QMenu, QFileDialog, 
    QStatusBar, QDialog, QMessageBox, QToolBar, QComboBox, QSplitter, QCheckBox, 
    QProgressBar, QListWidget, QListWidgetItem, QInputDialog, QToolButton, QSizePolicy
)
from PySide6.QtCore import Qt, QPoint, QUrl, QSettings, QTimer
from PySide6.QtGui import QFont, QAction, QKeySequence, QShortcut, QDesktopServices

# Expanded data structure: (Symbol, Name, Description, Example, LaTeX)
MATH_DATA = {
    "➕ Arithmetic": [
        ("+", "Plus", "Addition of two numbers", "2 + 2 = 4", r"+"),
        ("−", "Minus", "Subtraction of two numbers", "5 − 3 = 2", r"-"),
        ("×", "Multiplication", "Product of two numbers", "4 × 3 = 12", r"\times"),
        ("÷", "Division", "Quotient of two numbers", "10 ÷ 2 = 5", r"\div"),
        ("√", "Square Root", "A number that produces a specified quantity when multiplied by itself", "√9 = 3", r"\sqrt{}"),
        ("%", "Percentage", "A number or ratio expressed as a fraction of 100", "50% = 0.5", r"\%"),
        ("^", "Exponent", "Raised to the power of", "2^3 = 8", r"^{}"),
        ("±", "Plus-Minus", "Both positive and negative versions", "x = ±2", r"\pm"),
    ],
    "🧮 Algebra": [
        ("=", "Equals", "Indicates equality", "x = 5", r"="),
        ("≠", "Not Equal", "Indicates inequality", "x ≠ 5", r"\neq"),
        ("≈", "Approximately", "Roughly equal to", "π ≈ 3.14", r"\approx"),
        ("<", "Less Than", "Strictly smaller in value", "x < 10", r"<"),
        (">", "Greater Than", "Strictly larger in value", "x > 0", r">"),
        ("≤", "Less Than or Equal", "Smaller or equal to", "x ≤ 10", r"\leq"),
        ("≥", "Greater Than or Equal", "Larger or equal to", "x ≥ 0", r"\geq"),
        ("∝", "Proportional", "Changes with respect to", "y ∝ x", r"\propto"),
        ("⇒", "Implies", "Logical consequence (if A then B)", "x = 2 ⇒ x² = 4", r"\Rightarrow"),
    ],
    "📈 Calculus": [
        ("∫", "Integral", "Area under a curve; opposite of derivative", "∫f(x)dx", r"\int"),
        ("∂", "Partial Derivative", "Derivative of a function of multiple variables", "∂f/∂x", r"\partial"),
        ("d/dx", "Derivative", "Rate of change of a function", "d/dx (x²) = 2x", r"\frac{d}{dx}"),
        ("∑", "Summation", "Sum of a sequence of terms", "∑(i=1 to n) i", r"\sum"),
        ("∏", "Product", "Product of a sequence of terms", "∏(i=1 to n) i", r"\prod"),
        ("∞", "Infinity", "Without bound or limit", "lim x→∞", r"\infty"),
        ("lim", "Limit", "Value a function approaches", "lim(x→0) sin(x)/x = 1", r"\lim"),
    ],
    "🌐 Vector Calculus": [
        ("∇", "Nabla / Del", "Vector differential operator", "∇f (gradient)", r"\nabla"),
        ("∇·", "Divergence", "Measure of vector field source/sink", "∇·F", r"\nabla \cdot"),
        ("∇×", "Curl", "Rotation of a vector field", "∇×F", r"\nabla \times"),
        ("∇²", "Laplacian", "Divergence of the gradient of a function", "∇²f = 0 (Laplace eq)", r"\nabla^2"),
        ("∮", "Closed Integral", "Integral over a closed curve/surface", "∮ E · dl", r"\oint"),
        ("∯", "Surface Integral", "Integral over a closed surface", "∯ D · dA", r"\oiint"),
    ],
    "⚙️ Differential Eqs": [
        ("y'", "First Derivative", "Derivative of y w.r.t independent variable", "y' = dy/dx", r"y'"),
        ("ÿ", "Second Derivative", "Second derivative w.r.t time", "ÿ = -g", r"\ddot{y}"),
        ("𝒪", "Big O Notation", "Asymptotic upper bound complexity", "f(x) = 𝒪(g(x))", r"\mathcal{O}"),
        ("ℒ", "Laplace Transform", "Integral transform converting to s-domain", "ℒ{f(t)} = F(s)", r"\mathcal{L}"),
        ("ℱ", "Fourier Transform", "Decomposes function into frequencies", "ℱ{f(x)} = F(k)", r"\mathcal{F}"),
        ("δ", "Delta Function", "Generalized function zero except at zero", "∫δ(x)f(x)dx = f(0)", r"\delta"),
    ],
    "💠 Set Theory": [
        ("∈", "Element of", "Belongs to a set", "x ∈ A", r"\in"),
        ("∉", "Not Element of", "Does not belong to a set", "x ∉ A", r"\notin"),
        ("∪", "Union", "Combined elements of sets", "A ∪ B", r"\cup"),
        ("∩", "Intersection", "Common elements of sets", "A ∩ B", r"\cap"),
        ("∅", "Empty Set", "A set with no elements", "A = ∅", r"\emptyset"),
        ("⊂", "Proper Subset", "A is strictly within B", "A ⊂ B", r"\subset"),
        ("⊆", "Subset", "A is within or equal to B", "A ⊆ B", r"\subseteq"),
        ("ℝ", "Real Numbers", "Set of all real numbers", "x ∈ ℝ", r"\mathbb{R}"),
        ("ℕ", "Natural Numbers", "Set of positive integers", "n ∈ ℕ", r"\mathbb{N}"),
    ],
    "📐 Geometry": [
        ("∠", "Angle", "Formed by two rays", "∠ABC = 90°", r"\angle"),
        ("⊥", "Perpendicular", "At right angles to", "AB ⊥ CD", r"\perp"),
        ("∥", "Parallel", "Never intersecting", "AB ∥ CD", r"\parallel"),
        ("△", "Triangle", "Three-sided polygon", "△ABC", r"\triangle"),
        ("○", "Circle", "Set of points equidistant from a center", "○O", r"\circle"),
        ("≅", "Congruent", "Same shape and size", "△ABC ≅ △DEF", r"\cong"),
        ("~", "Similar", "Same shape, different size", "△ABC ~ △DEF", r"\sim"),
        ("π", "Pi", "Ratio of circumference to diameter", "π ≈ 3.14159", r"\pi"),
    ],
    "🧠 Logic": [
        ("∀", "For All", "Universal quantification", "∀x ∈ ℝ, x² ≥ 0", r"\forall"),
        ("∃", "There Exists", "Existential quantification", "∃x ∈ ℝ, x > 5", r"\exists"),
        ("¬", "Not", "Logical negation", "¬(A ∧ B)", r"\neg"),
        ("∧", "And", "Logical conjunction", "A ∧ B", r"\wedge"),
        ("∨", "Or", "Logical disjunction", "A ∨ B", r"\vee"),
        ("⇔", "If and Only If", "Biconditional logical connective", "A ⇔ B", r"\Leftrightarrow"),
        ("∴", "Therefore", "Logical conclusion", "A = B, B = C ∴ A = C", r"\therefore"),
    ],
    "📉 Trigonometry": [
        ("sin", "Sine", "Ratio of opposite to hypotenuse", "sin(θ) = opp/hyp", r"\sin"),
        ("cos", "Cosine", "Ratio of adjacent to hypotenuse", "cos(θ) = adj/hyp", r"\cos"),
        ("tan", "Tangent", "Ratio of opposite to adjacent", "tan(θ) = opp/adj", r"\tan"),
        ("θ", "Theta", "Standard angle variable", "sin(θ)² + cos(θ)² = 1", r"\theta"),
        ("csc", "Cosecant", "Reciprocal of sine", "csc(θ) = 1/sin(θ)", r"\csc"),
        ("sec", "Secant", "Reciprocal of cosine", "sec(θ) = 1/cos(θ)", r"\sec"),
        ("cot", "Cotangent", "Reciprocal of tangent", "cot(θ) = 1/tan(θ)", r"\cot"),
    ],
    "🟩 Linear Algebra": [
        ("v", "Vector", "Quantity with magnitude and direction", "v = [x, y, z]", r"\vec{v}"),
        ("A", "Matrix", "Rectangular array of numbers", "A = [[1, 2], [3, 4]]", r"\mathbf{A}"),
        ("·", "Dot Product", "Sum of products of corresponding entries", "a · b", r"\cdot"),
        ("⊗", "Tensor Product", "Kronecker product of two matrices", "A ⊗ B", r"\otimes"),
        ("det", "Determinant", "Scalar value of a square matrix", "det(A)", r"\det"),
        ("λ", "Eigenvalue", "Scalar associated with linear transformations", "Av = λv", r"\lambda"),
        ("T", "Transpose", "Matrix flipped over its diagonal", "Aᵀ", r"^T"),
    ],
    "📊 Probability & Stats": [
        ("P(A)", "Probability", "Likelihood of event A occurring", "P(A) = 0.5", r"P(A)"),
        ("E(X)", "Expected Value", "Long-run average value of repetitions", "E(X) = μ", r"E(X)"),
        ("μ", "Mean", "Average of a set of numbers", "μ = Σx/n", r"\mu"),
        ("σ", "Standard Deviation", "Measure of amount of variation", "σ² = Variance", r"\sigma"),
        ("σ²", "Variance", "Expectation of squared deviation", "σ² = E[(X-μ)²]", r"\sigma^2"),
        ("X ~ N", "Distribution", "Variable X is normally distributed", "X ~ N(μ, σ²)", r"\sim"),
        ("x̂", "Estimator", "Estimated value of parameter x", "x̂ = 10.5", r"\hat{x}"),
    ],
    "🔢 Number Theory": [
        ("≡", "Congruent", "Numbers with same remainder when divided", "a ≡ b (mod n)", r"\equiv"),
        ("mod", "Modulo", "Remainder after division", "10 mod 3 = 1", r"\mod"),
        ("|", "Divides", "a divides b evenly", "a | b", r"\mid"),
        ("∤", "Does Not Divide", "a does not divide b evenly", "a ∤ b", r"\nmid"),
        ("gcd", "GCD", "Greatest Common Divisor", "gcd(8, 12) = 4", r"\gcd"),
        ("ℤ", "Integers", "Set of all positive and negative whole numbers", "z ∈ ℤ", r"\mathbb{Z}"),
        ("ℚ", "Rationals", "Set of numbers expressed as fractions", "q ∈ ℚ", r"\mathbb{Q}"),
    ],
    "🎲 Combinatorics": [
        ("n!", "Factorial", "Product of all positive integers up to n", "5! = 120", r"!"),
        ("nPr", "Permutation", "Arrangements of n items taken r at a time", "5P2 = 20", r"P(n,r)"),
        ("nCr", "Combination", "Selections of n items taken r at a time", "5C2 = 10", r"\binom{n}{r}"),
        ("|S|", "Cardinality", "Number of elements in set S", "|{1,2}| = 2", r"|S|"),
        ("P(n,k)", "k-Permutation", "Ordered arrangement of k elements from n", "P(5,2) = 20", r"P(n,k)"),
    ],
    "🍝 Graph Theory": [
        ("G=(V,E)", "Graph", "Consists of vertices (V) and edges (E)", "G = ({1,2}, {{1,2}})", r"G=(V,E)"),
        ("deg(v)", "Degree", "Number of edges incident to vertex v", "deg(v) = 3", r"\deg(v)"),
        ("Kₙ", "Complete Graph", "Graph where every pair of vertices is connected", "K₅ has 10 edges", r"K_n"),
        ("δ(G)", "Min Degree", "Smallest degree of any vertex in G", "δ(G) = 2", r"\delta(G)"),
        ("Δ(G)", "Max Degree", "Largest degree of any vertex in G", "Δ(G) = 5", r"\Delta(G)"),
        ("χ(G)", "Chromatic Number", "Minimum colors needed to color G", "χ(K₃) = 3", r"\chi(G)"),
    ],
    "🧭 Topology": [
        ("∂A", "Boundary", "Set of points that can be approached from both inside and outside A", "∂A = cl(A) ∩ cl(X\\A)", r"\partial A"),
        ("int(A)", "Interior", "Set of all interior points of A", "int(A) ⊆ A", r"\text{int}(A)"),
        ("cl(A)", "Closure", "Smallest closed set containing A", "cl(A) = A ∪ ∂A", r"\text{cl}(A)"),
        ("≅", "Homeomorphic", "Topologically equivalent spaces", "Mug ≅ Donut", r"\cong"),
        ("τ", "Topology", "Collection of open sets satisfying certain axioms", "(X, τ)", r"\tau"),
        ("X × Y", "Product Space", "Topological product of two spaces", "ℝ × ℝ = ℝ²", r"\times"),
    ],
    "🔗 Category Theory": [
        ("f: A → B", "Morphism", "An arrow from object A to object B in a category", "f: X → Y", r"f: A \to B"),
        ("∘", "Composition", "Combining two morphisms", "g ∘ f", r"\circ"),
        ("idₐ", "Identity Morphism", "Arrow from an object to itself", "idₐ ∘ f = f", r"id_A"),
        ("F: C → D", "Functor", "Maps objects and morphisms between categories", "F(f)", r"F: C \to D"),
        ("Obj(C)", "Objects", "The class of all objects in category C", "A ∈ Obj(C)", r"\text{Obj}(C)"),
        ("Hom(A,B)", "Hom-Set", "Set of all morphisms from A to B", "f ∈ Hom(A,B)", r"\text{Hom}(A,B)"),
    ],
    "⛓️ Sequences & Series": [
        ("aₙ", "Sequence Term", "The n-th term of a sequence", "aₙ = 2n", r"a_n"),
        ("aₙ → L", "Converges", "A sequence approaches a limit L", "aₙ → 0", r"\to"),
        ("Σaₙ", "Series", "Sum of the terms of a sequence", "Σ(1/n²) = π²/6", r"\sum"),
        ("cauchy", "Cauchy Seq", "Sequence where terms become arbitrarily close", "Every conv. seq is Cauchy", r"\text{cauchy}"),
        ("aₙ₊₁", "Recursive", "Next term defined by previous term(s)", "aₙ₊₁ = aₙ + 1", r"a_{n+1}"),
        ("∑", "Summation", "Adding up a sequence of numbers", "∑ iⁿ", r"\sum"),
    ],
    "🚦 Boolean Algebra": [
        ("⊕", "XOR", "Exclusive OR (true if exactly one is true)", "A ⊕ B", r"\oplus"),
        ("⊼", "NAND", "NOT AND (false only if both are true)", "A ⊼ B", r"\barwedge"),
        ("⊽", "NOR", "NOT OR (true only if both are false)", "A ⊽ B", r"\veebar"),
        ("⊤", "Tautology", "A statement that is always true", "A ∨ ¬A = ⊤", r"\top"),
        ("⊥", "Contradiction", "A statement that is always false", "A ∧ ¬A = ⊥", r"\bot"),
        ("⊨", "Entails", "Logical consequence / semantic entailment", "A ⊨ B", r"\models"),
    ],
    "❄️ Fractals & Chaos": [
        ("dim_H", "Hausdorff Dim", "Fractional dimension of a geometric object", "dim_H(Cantor) = 0.63", r"dim_H"),
        ("λ", "Lyapunov Exp", "Rate of separation of infinitesimally close trajectories", "λ > 0 implies chaos", r"\lambda"),
        ("M", "Mandelbrot Set", "Set of complex numbers for which f(z)=z²+c does not diverge", "zₙ₊₁ = zₙ² + c", r"M"),
        ("fⁿ", "Iterated Func", "Function composed with itself n times", "f²(x) = f(f(x))", r"f^n"),
    ],
    "♟️ Game Theory": [
        ("NE", "Nash Equilibrium", "Set of strategies where no player benefits by changing unilaterally", "Find NE in payoff matrix", r"NE"),
        ("Σuᵢ = 0", "Zero-Sum", "One player's gain is exactly another's loss", "Σuᵢ = 0", r"\sum u_i = 0"),
        ("πᵢ", "Payoff", "Reward received by player i", "π₁(A, B) = 5", r"\pi_i"),
        ("≻", "Preference", "Strict preference relation", "A ≻ B", r"\succ"),
        ("σ", "Mixed Strategy", "Probability distribution over pure strategies", "σ = (0.5, 0.5)", r"\sigma"),
    ],
    "🎯 Optimization": [
        ("argmin", "Argument Min", "Value of x that minimizes function f(x)", "argmin f(x)", r"\arg\min"),
        ("argmax", "Argument Max", "Value of x that maximizes function f(x)", "argmax f(x)", r"\arg\max"),
        ("s.t.", "Subject To", "Constraints applied to an optimization problem", "min f(x) s.t. g(x)≤0", r"\text{s.t.}"),
        ("f*", "Global Optimum", "The absolute minimum or maximum value of f", "f* = 0", r"f^*"),
        ("∇f=0", "Stationary Point", "Point where gradient is zero (local extremum)", "∇f(x₀) = 0", r"\nabla f = 0"),
    ],
    "💾 Information Theory": [
        ("H(X)", "Entropy", "Average rate at which information is produced by random source", "H(X) = -Σp(x)log p(x)", r"H(X)"),
        ("I(X;Y)", "Mutual Info", "Amount of information obtained about one random variable by observing another", "I(X;Y) ≥ 0", r"I(X;Y)"),
        ("D_KL", "KL Divergence", "Measure of how one probability distribution differs from another", "D_KL(P||Q)", r"D_{KL}"),
        ("H(P|Q)", "Cross-Entropy", "Average number of bits needed to encode events from P using Q", "H(P,Q) = H(P) + D_KL", r"H(P,Q)"),
    ],
    "🧊 Tensor Calculus": [
        ("Γᵏᵢⱼ", "Christoffel Sym", "Connection coefficients describing curvature in coordinates", "Γᵏᵢⱼ = ½ gᵏˡ(∂...)", r"\Gamma^k_{ij}"),
        ("gᵢⱼ", "Metric Tensor", "Defines distances and angles in a given space", "ds² = gᵢⱼ dxⁱ dxʲ", r"g_{ij}"),
        ("∇ᵢ", "Covariant Deriv", "Derivative that accounts for curvature of space", "∇ᵢ Vʲ", r"\nabla_i"),
        ("Rᵢⱼₖₗ", "Riemann Tensor", "Mathematical object describing intrinsic curvature of space", "Rᵢⱼₖₗ", r"R_{ijkl}"),
        ("Einstein Sum", "Summation Convention", "Implicit summation over repeated indices", "aᵢbⁱ = Σ aᵢbⁱ", r"\text{Einstein}"),
    ],
    "🔤 Greek Alphabet": [
        ("α", "Alpha", "Commonly used for angles or significance level", "α = 0.05", r"\alpha"),
        ("β", "Beta", "Commonly used for angles or coefficients", "β₁", r"\beta"),
        ("γ", "Gamma", "Gamma function or angles", "γ = 90°", r"\gamma"),
        ("δ", "Delta", "Change or difference", "δx = x₂ - x₁", r"\delta"),
        ("ε", "Epsilon", "Very small positive quantity", "lim x→ε", r"\epsilon"),
        ("λ", "Lambda", "Wavelength or eigenvalues", "λ = c/f", r"\lambda"),
        ("Σ", "Sigma (Cap)", "Summation operator", "Σ xᵢ", r"\Sigma"),
        ("Φ", "Phi (Cap)", "Golden ratio", "Φ = (1+√5)/2", r"\Phi"),
        ("Ω", "Omega (Cap)", "Ohms or sample space in probability", "P(Ω) = 1", r"\Omega"),
    ],
    "🌀 Complex Analysis": [
        ("ℂ", "Complex Numbers", "Set of all numbers with real and imaginary parts", "z ∈ ℂ", r"\mathbb{C}"),
        ("Re(z)", "Real Part", "The real component of a complex number", "Re(3+4i) = 3", r"\text{Re}(z)"),
        ("Im(z)", "Imaginary Part", "The imaginary component of a complex number", "Im(3+4i) = 4", r"\text{Im}(z)"),
        ("|z|", "Modulus", "Magnitude of a complex number from origin", "|3+4i| = 5", r"|z|"),
        ("arg(z)", "Argument", "Angle of the complex number in the complex plane", "arg(1+i) = π/4", r"\arg(z)"),
        ("z*", "Complex Conjugate", "Complex number with negated imaginary part", "(3+4i)* = 3-4i", r"\bar{z}"),
        ("i", "Imaginary Unit", "Square root of -1", "i² = -1", r"i"),
    ],
    "🧩 Abstract Algebra": [
        ("G", "Group", "A set with an operation satisfying closure, associativity, identity, and invertibility", "(G, ⋅)", r"G"),
        ("e", "Identity Element", "The element that leaves other elements unchanged under the operation", "e ⋅ a = a", r"e"),
        ("a⁻¹", "Inverse Element", "The element that yields the identity when combined with a", "a ⋅ a⁻¹ = e", r"a^{-1}"),
        ("|G|", "Order of Group", "The number of elements in the group G", "|ℤ₅| = 5", r"|G|"),
        ("H ≤ G", "Subgroup", "A subset H that is itself a group under the operation of G", "2ℤ ≤ ℤ", r"H \leq G"),
        ("Ker(φ)", "Kernel", "The set of elements mapped to the identity by a homomorphism", "Ker(φ) = {g ∈ G : φ(g) = e}", r"\text{Ker}(\phi)"),
        ("Im(φ)", "Image", "The set of outputs of a group homomorphism", "Im(φ) ≤ H", r"\text{Im}(\phi)"),
    ],
    "💰 Financial Math": [
        ("PV", "Present Value", "Current value of a future sum of money discounted at a rate", "PV = FV / (1+r)ⁿ", r"PV"),
        ("FV", "Future Value", "Value of an asset at a future date based on an assumed growth rate", "FV = PV(1+r)ⁿ", r"FV"),
        ("r", "Interest Rate", "Proportion of a loan charged as interest to the borrower", "r = 5%", r"r"),
        ("σ", "Volatility", "Degree of variation of a trading price series over time", "σ = 0.2", r"\sigma"),
        ("Δ", "Delta", "Ratio of change in option price to change in underlying asset price", "Δ = 0.5", r"\Delta"),
        ("E[R]", "Expected Return", "Anticipated return on an investment", "E[R] = Σ p_i R_i", r"E[R]"),
        ("β", "Beta", "Measure of a stock's volatility relative to the market", "β = 1.2", r"\beta"),
    ],
    "🧪 Numerical Analysis": [
        ("O(h)", "Big O Error", "Error term proportional to step size h", "f'(x) = (f(x+h)-f(x))/h + O(h)", r"O(h)"),
        ("Δx", "Step Size", "Increment between discrete points in a numerical method", "xₙ₊₁ = xₙ + Δx", r"\Delta x"),
        ("‖A‖", "Matrix Norm", "A function that assigns a strictly positive length/size to a matrix", "‖A‖₂", r"\|A\|"),
        ("cond(A)", "Condition Number", "Measures how sensitive a function's output is to changes in input", "cond(A) = ‖A‖‖A⁻¹‖", r"\text{cond}(A)"),
        ("fₙ", "Iterative Approx", "n-th approximation in an iterative sequence", "xₙ₊₁ = g(xₙ)", r"f_n"),
    ],
    "📏 Measure Theory": [
        ("μ", "Measure", "A function that assigns a number to subsets of a space", "μ([0,1]) = 1", r"\mu"),
        ("Σ", "Sigma-Algebra", "A collection of subsets closed under complement and countable unions", "(X, Σ)", r"\Sigma"),
        ("a.e.", "Almost Everywhere", "A property holds everywhere except on a set of measure zero", "f = 0 a.e.", r"\text{a.e.}"),
        ("∫fdμ", "Lebesgue Int", "Generalization of the Riemann integral", "∫_X f dμ", r"\int f d\mu"),
        ("Lᵖ", "Lp Space", "Function spaces defined using a generalization of the p-norm", "f ∈ L²(ℝ)", r"L^p"),
    ],
    "🔐 Cryptography": [
        ("p ⊕ q", "XOR Cipher", "Bitwise exclusive OR operation used in encryption", "p ⊕ k = c", r"\oplus"),
        ("N = pq", "RSA Modulus", "Product of two large primes used in RSA algorithm", "N = 61 × 53", r"N = pq"),
        ("φ(n)", "Euler's Totient", "Count of numbers up to n that are coprime with n", "φ(9) = 6", r"\phi(n)"),
        ("H(x)", "Hash Function", "A one-way function mapping data of arbitrary size to fixed-size values", "H('abc') = '...'", r"H(x)"),
        ("d(e(c))", "Decryption", "Applying decryption key d to ciphertext c to get plaintext", "d(e(m)) = m", r"d(e(c))"),
        ("PRNG", "Pseudo-Random", "Algorithm for generating a sequence of numbers approximating random", "PRNG(seed)", r"\text{PRNG}"),
    ],
    "⚛️ Quantum Mechanics": [
        ("|ψ⟩", "Ket", "Quantum state vector", "|ψ⟩ = a|0⟩ + b|1⟩", r"|\psi\rangle"),
        ("⟨φ|", "Bra", "Dual vector corresponding to a ket", "⟨φ|ψ⟩", r"\langle\phi|"),
        ("⟨φ|ψ⟩", "Inner Product", "Probability amplitude of measuring state ψ as φ", "⟨φ|ψ⟩ = ∫φ*ψ dx", r"\langle\phi|\psi\rangle"),
        ("Ĥ", "Hamiltonian", "Operator corresponding to total energy of the system", "Ĥ|ψ⟩ = E|ψ⟩", r"\hat{H}"),
        ("[A, B]", "Commutator", "Measure of failure of two operations to commute", "[A, B] = AB - BA", r"[A, B]"),
        ("ℏ", "Reduced Planck", "Planck constant divided by 2π", "E = ℏω", r"\hbar"),
    ],
    "🛰️ Differential Geometry": [
        ("M", "Manifold", "Topological space that locally resembles Euclidean space", "Mⁿ", r"M"),
        ("TₚM", "Tangent Space", "Vector space of tangent vectors at point p", "v ∈ TₚM", r"T_pM"),
        ("ℒ_X Y", "Lie Derivative", "Derivative of a tensor field along a vector field", "ℒ_X Y = [X, Y]", r"\mathcal{L}_X Y"),
        ("R(X,Y)Z", "Riemann Curv", "Measures how curved a manifold is", "R(X,Y)Z = ∇_X∇_Y Z - ...", r"R(X,Y)Z"),
        ("ds²", "Line Element", "Infinitesimal distance along a curve", "ds² = gᵢⱼdxⁱdxʲ", r"ds^2"),
        ("∇", "Affine Connection", "Rule for parallel transport of vectors", "∇ᵢVⱼ", r"\nabla_i"),
    ],
    "✨ Special Functions": [
        ("Γ(z)", "Gamma Function", "Extension of factorial to complex numbers", "Γ(n) = (n-1)! for integers", r"\Gamma(z)"),
        ("ζ(s)", "Riemann Zeta", "Sum of inverse powers, central to prime distribution", "ζ(2) = π²/6", r"\zeta(s)"),
        ("Jₙ(x)", "Bessel Function", "Solutions to Bessel's differential equation", "J₀(0) = 1", r"J_n(x)"),
        ("erf(x)", "Error Function", "Integral of the Gaussian distribution", "erf(∞) = 1", r"\text{erf}(x)"),
        ("B(x,y)", "Beta Function", "Integral related to Gamma function", "B(x,y) = Γ(x)Γ(y)/Γ(x+y)", r"B(x,y)"),
    ],
    "💻 Algorithms & Complexity": [
        ("O(g(n))", "Big O", "Asymptotic upper bound on time/space complexity", "Merge sort is O(n log n)", r"O(g(n))"),
        ("Ω(g(n))", "Big Omega", "Asymptotic lower bound on complexity", "Comparison sort is Ω(n)", r"\Omega(g(n))"),
        ("Θ(g(n))", "Big Theta", "Tight asymptotic bound on complexity", "Binary search is Θ(log n)", r"\Theta(g(n))"),
        ("P", "Polynomial Time", "Class of problems solvable deterministically in poly time", "P ⊆ NP", r"P"),
        ("NP", "Nondeterministic Poly", "Problems verifiable in polynomial time", "SAT is in NP", r"NP"),
        ("NP-Hard", "At least as hard as NP", "Problems to which all NP problems can be reduced", "TSP is NP-Hard", r"\text{NP-Hard}"),
    ],
    "🎲 Stochastic Processes": [
        ("Xₜ", "Stochastic Process", "Collection of random variables indexed by time", "{Xₜ : t ≥ 0}", r"X_t"),
        ("Pᵢⱼ", "Transition Prob", "Probability of moving from state i to j in Markov chain", "P(Xₙ₊₁=j | Xₙ=i) = Pᵢⱼ", r"P_{ij}"),
        ("λ", "Poisson Rate", "Average number of events per interval in a Poisson process", "P(k) = (λᵏe⁻ᵘ)/k!", r"\lambda"),
        ("Wₜ", "Wiener Process", "Mathematical model of Brownian motion", "Wₜ ~ N(0, t)", r"W_t"),
        ("π", "Stationary Dist", "Long-run probability distribution of a Markov chain", "π = πP", r"\pi"),
    ],
    "🧬 Knot Theory": [
        ("Kₙ", "Knot Invariant", "A quantity defined for each knot that is the same for equivalent knots", "Kₜ(A) = Kₜ(B)", r"K_n"),
        ("Lk(A,B)", "Linking Number", "An integer invariant describing the degree of linking of two components", "Lk(A,B) = +1", r"\text{Lk}(A,B)"),
        ("σ(K)", "Knot Signature", "An integer invariant computed from the Seifert matrix", "σ(Unknot) = 0", r"\sigma(K)"),
        ("Unknot", "Trivial Knot", "A knot that is equivalent to a standard circle in 3D space", "Ring without crossings", r"\text{Unknot}"),
        ("V_K(t)", "Jones Polynomial", "A polynomial invariant of knots that can distinguish chirality", "V_Unknot(t) = 1", r"V_K(t)"),
        ("c(K)", "Crossing Number", "The minimum number of crossings in any diagram of the knot", "c(Trefoil) = 3", r"c(K)"),
    ],
    "🌌 Cosmology & Astrophysics": [
        ("H₀", "Hubble Constant", "Rate of expansion of the universe (km/s/Mpc)", "H₀ ≈ 70 km/s/Mpc", r"H_0"),
        ("ρ_c", "Critical Density", "Density required for the universe to be flat", "ρ_c = 3H²/8πG", r"\rho_c"),
        ("Ω", "Density Parameter", "Ratio of actual density to critical density", "Ω = ρ/ρ_c", r"\Omega"),
        ("r_s", "Schwarzschild Radius", "Radius of the event horizon of a non-rotating black hole", "r_s = 2GM/c²", r"r_s"),
        ("z", "Redshift", "Shift of spectral lines toward longer wavelengths due to expansion", "z = (λ_obs - λ_emit)/λ_emit", r"z"),
        ("Λ", "Cosmological Constant", "Energy density of space (dark energy)", "Λ ≈ 1.1 × 10⁻⁵² m⁻²", r"\Lambda"),
    ],
    "🦠 Math Biology": [
        ("R₀", "Basic Reproduction", "Expected number of cases directly generated by one case", "R₀ > 1 means epidemic", r"R_0"),
        ("SIR", "SIR Model", "Compartmental model for disease spread (Susceptible, Infected, Recovered)", "dS/dt = -βSI", r"\text{SIR}"),
        ("K", "Carrying Capacity", "Maximum population size an environment can sustain", "dN/dt = rN(1 - N/K)", r"K"),
        ("α", "Predation Rate", "Rate at which predators consume prey in Lotka-Volterra", "dP/dt = αPQ - βP", r"\alpha"),
        ("β", "Contact Rate", "Rate of infection in epidemiological models", "dI/dt = βSI - γI", r"\beta"),
        ("γ", "Recovery Rate", "Rate at which infected individuals recover", "dR/dt = γI", r"\gamma"),
    ],
    "🧿 Differential Forms": [
        ("∧", "Wedge Product", "Antisymmetric product of differential forms", "dx ∧ dy = -dy ∧ dx", r"\wedge"),
        ("d", "Exterior Derivative", "Generalization of the differential to forms", "d(df) = 0", r"d"),
        ("*", "Hodge Star", "Operator mapping p-forms to (n-p)-forms", "*dx = dy", r"\star"),
        ("Ωᵖ(M)", "Space of p-forms", "Vector space of differential p-forms on a manifold M", "ω ∈ Ω²(ℝ³)", r"\Omega^p(M)"),
        ("dω = 0", "Closed Form", "A differential form whose exterior derivative is zero", "dω = 0", r"d\omega = 0"),
        ("dω = α", "Exact Form", "A form that is the exterior derivative of another form", "ω = dα", r"d\omega = \alpha"),
    ],
    "🏛️ Famous Constants": [
        ("e", "Euler's Number", "Base of the natural logarithm", "e ≈ 2.71828", r"e"),
        ("γ", "Euler-Mascheroni", "Limit of the difference between harmonic series and natural log", "γ ≈ 0.57721", r"\gamma"),
        ("τ", "Tau", "Ratio of circumference to radius (2π)", "τ = 2π ≈ 6.28318", r"\tau"),
        ("G", "Catalan's Constant", "Value of the Dirichlet beta function at 2", "G ≈ 0.91596", r"G"),
        ("A", "Glaisher-Kinkelin", "Constant appearing in asymptotic formulas for factorials", "A ≈ 1.28243", r"A"),
        ("C₄", "Lemniscate Constant", "Ratio of perimeter of Bernoulli lemniscate to its diameter", "C₄ ≈ 2.62206", r"C_4"),
    ],
    "🌊 Fluid Dynamics": [
        ("Re", "Reynolds Number", "Ratio of inertial to viscous forces", "Re = ρvL/μ", r"\text{Re}"),
        ("∇·v = 0", "Incompressibility", "Continuity equation for constant density fluids", "∂v/∂x = 0", r"\nabla \cdot \mathbf{v} = 0"),
        ("ρ", "Density", "Mass per unit volume of a fluid", "ρ = m/V", r"\rho"),
        ("μ", "Dynamic Viscosity", "Measure of a fluid's resistance to flow", "τ = μ(du/dy)", r"\mu"),
        ("ν", "Kinematic Viscosity", "Ratio of dynamic viscosity to density", "ν = μ/ρ", r"\nu"),
        ("τ", "Shear Stress", "Force per unit area parallel to the surface", "τ = F/A", r"\tau"),
    ],
    "🌡️ Thermodynamics": [
        ("S", "Entropy", "Measure of disorder or randomness in a system", "dS = dQ/T", r"S"),
        ("k_B", "Boltzmann Constant", "Relates temperature to energy of gas particles", "E = k_B T", r"k_B"),
        ("Z", "Partition Function", "Sum over all statistical states of a system", "Z = Σe^(-βEᵢ)", r"Z"),
        ("β", "Thermodynamic Beta", "Inverse temperature (1/kT)", "β = 1/(k_B T)", r"\beta"),
        ("μ", "Chemical Potential", "Change in free energy per added particle", "μ = (∂G/∂N)", r"\mu"),
        ("U", "Internal Energy", "Total energy contained within a thermodynamic system", "dU = TdS - PdV", r"U"),
    ],
    "📻 Signal Processing": [
        ("f_s", "Sampling Freq", "Number of samples per second", "f_s > 2f_max", r"f_s"),
        ("f_N", "Nyquist Rate", "Minimum sampling rate to avoid aliasing", "f_N = 2f_max", r"f_N"),
        ("*", "Convolution", "Mathematical operation on two functions producing a third", "(f * g)(t)", r"*"),
        ("h(t)", "Impulse Response", "Output of a system when presented with a brief input signal", "y(t) = x(t) * h(t)", r"h(t)"),
        ("X(e^jω)", "DTFT", "Discrete-Time Fourier Transform", "X(e^jω) = Σx[n]e^-jωn", r"X(e^{j\omega})"),
        ("SNR", "Signal-to-Noise", "Ratio of signal power to noise power", "SNR = 10 log10(P_s/P_n)", r"\text{SNR}"),
    ],
    "🔢 Number Bases": [
        ("0b", "Binary", "Base-2 numeral system", "0b1010 = 10", r"0b_2"),
        ("0x", "Hexadecimal", "Base-16 numeral system", "0xFF = 255", r"0x_{16}"),
        ("0o", "Octal", "Base-8 numeral system", "0o17 = 15", r"0o_8"),
        ("log_b", "Logarithm Base", "Inverse of exponentiation for base b", "log_2(8) = 3", r"\log_b"),
        ("N_b", "Base-b Notation", "Number N represented in base b", "1010_2", r"N_b"),
    ],
    "🗺️ Metric Spaces": [
        ("d(x, y)", "Metric", "Distance function satisfying positivity, symmetry, and triangle ineq", "d(x,y) = |x-y|", r"d(x, y)"),
        ("B(x, r)", "Open Ball", "Set of points within distance r from center x", "B(x, r) = {y : d(x,y)<r}", r"B(x, r)"),
        ("||x||_p", "Lp Norm", "Generalization of vector length for p-norms", "||x||_1 = Σ|xᵢ|", r"\|x\|_p"),
        ("d", "Distance", "Scalar measure of space between two points", "d = √(Δx² + Δy²)", r"d"),
        ("C_b(X)", "Bounded Cont. Funcs", "Space of all bounded continuous functions on X", "f ∈ C_b([0,1])", r"C_b(X)"),
        ("Cmpl", "Complete Metric", "Metric space where every Cauchy sequence converges", "(ℝ, |·|) is Cmpl", r"\text{Cmpl}"),
    ],
    "🏔️ Calculus of Variations": [
        ("J[y]", "Functional", "Maps functions to real numbers, often representing action or energy", "J[y] = ∫ L(x,y,y') dx", r"J[y]"),
        ("δJ", "Variation", "Infinitesimal change in a functional", "δJ = 0", r"\delta J"),
        ("∂L/∂y", "Euler-Lagrange", "Necessary condition for a functional to be stationary", "d/dx(∂L/∂y') - ∂L/∂y = 0", r"\frac{\partial L}{\partial y}"),
        ("p", "Conjugate Momentum", "Momentum corresponding to a generalized coordinate", "p = ∂L/∂ẋ", r"p"),
        ("λ", "Lagrange Multiplier", "Used to find extrema of functions subject to constraints", "∇f = λ∇g", r"\lambda"),
        ("I[y]", "Action Integral", "Integral of the Lagrangian over time", "I = ∫ (T - V) dt", r"I[y]"),
    ],
    "🎼 Harmonic Analysis": [
        ("â_n", "Fourier Coeff", "Coefficients representing the amplitude of harmonic frequencies", "â_n = 1/T ∫f(t)e^-iωnt dt", r"\hat{a}_n"),
        ("D_N(x)", "Dirichlet Kernel", "Kernel whose convolution with a function gives Fourier partial sum", "D_N(x) = Σe^inx", r"D_N(x)"),
        ("Pf", "Plancherel", "Theorem stating energy is preserved in Fourier transform", "∫|f|² = 2π∫|f̂|²", r"\mathcal{P}f"),
        ("Hf", "Hilbert Transform", "Linear operator that shifts the phase of negative frequencies by 90°", "Hf(t) = (1/π)PV∫f(τ)/(t-τ) dτ", r"Hf"),
        ("f̂(ξ)", "Fourier Transform", "Decomposes a function into its constituent frequencies", "f̂(ξ) = ∫f(x)e^-2πixξ dx", r"\hat{f}(\xi)"),
        ("S_N(f)", "Partial Sum", "Sum of the first N terms of a Fourier series", "S_N = Σâ_n e^inx", r"S_N(f)"),
    ],
    "🏗️ Finite Element Method (FEM)": [
        ("K", "Stiffness Matrix", "Matrix relating forces to displacements in a discrete system", "Ku = F", r"K"),
        ("u_h", "Discrete Solution", "Approximate solution defined on a finite element mesh", "u_h ∈ V_h", r"u_h"),
        ("φ_i", "Basis Function", "Locally supported functions used to approximate the solution", "u_h = Σu_i φ_i", r"\phi_i"),
        ("a(u,v)", "Bilinear Form", "Inner product like operator defining the weak formulation", "a(u,v) = ∫∇u·∇v dx", r"a(u,v)"),
        ("L(v)", "Linear Functional", "Right hand side of the weak formulation", "L(v) = ∫fv dx", r"L(v)"),
        ("h", "Mesh Size", "Characteristic length of elements in the mesh", "h → 0", r"h"),
    ],
    "🧲 Electromagnetism": [
        ("ε₀", "Permittivity", "Measure of resistance to forming an electric field in a vacuum", "ε₀ ≈ 8.85e-12 F/m", r"\varepsilon_0"),
        ("μ₀", "Permeability", "Measure of magnetization in response to a magnetic field", "μ₀ = 4π × 10⁻⁷ H/m", r"\mu_0"),
        ("∇×E", "Faraday's Law", "Induced electric field is proportional to rate of change of magnetic field", "∇×E = -∂B/∂t", r"\nabla \times \mathbf{E}"),
        ("∇×B", "Ampere's Law", "Magnetic field generated by current and changing electric field", "∇×B = μ₀J + μ₀ε₀∂E/∂t", r"\nabla \times \mathbf{B}"),
        ("F = qv×B", "Lorentz Force", "Force on a charged particle moving through electric and magnetic fields", "F = q(E + v×B)", r"\mathbf{F} = q\mathbf{v} \times \mathbf{B}"),
        ("ρ_v", "Charge Density", "Electric charge per unit volume", "ρ_v = dQ/dV", r"\rho_v"),
    ],
    "🧮 Discrete Math": [
        ("⌊x⌋", "Floor", "Greatest integer less than or equal to x", "⌊3.7⌋ = 3", r"\lfloor x \rfloor"),
        ("⌈x⌉", "Ceiling", "Smallest integer greater than or equal to x", "⌈3.2⌉ = 4", r"\lceil x \rceil"),
        ("n!!", "Double Factorial", "Product of all integers from 1 to n with same parity", "5!! = 5 × 3 × 1 = 15", r"n!!"),
        ("S(n,k)", "Stirling Number", "Number of ways to partition n objects into k non-empty sets", "S(4,2) = 7", r"S(n,k)"),
        ("B_n", "Bell Number", "Total number of partitions of a set of size n", "B_3 = 5", r"B_n"),
        ("!n", "Derangement", "Permutation where no element appears in its original position", "!3 = 2", r"!n"),
    ],
    # --- NEW CATEGORIES START ---
    "🤖 Machine Learning": [
        ("ReLU(x)", "Rectified Linear Unit", "Activation function defined as max(0, x)", "ReLU(-2) = 0", r"\text{ReLU}(x)"),
        ("σ(z)", "Sigmoid", "Squashes values to range (0, 1) for binary classification", "σ(z) = 1 / (1 + e^-z)", r"\sigma(z)"),
        ("∇J(θ)", "Gradient", "Vector of partial derivatives of the cost function J", "θ := θ - α∇J(θ)", r"\nabla J(\theta)"),
        ("CE", "Cross-Entropy Loss", "Loss function for classification, measuring divergence of distributions", "CE = -Σy log(ŷ)", r"\text{CE}"),
        ("W", "Weights", "Parameters in a neural network that transform input data", "y = Wx + b", r"\mathbf{W}"),
        ("b", "Bias", "Offset parameter added to the weighted sum in a neuron", "y = Wx + b", r"\mathbf{b}"),
        ("t-SNE", "Dimensionality Reduction", "Non-linear technique for embedding high-dim data for visualization", "t-SNE(X)", r"\text{t-SNE}"),
    ],
    "🧱 Lattice Theory": [
        ("∨", "Join", "Least upper bound (supremum) of two elements in a lattice", "a ∨ b", r"\vee"),
        ("∧", "Meet", "Greatest lower bound (infimum) of two elements in a lattice", "a ∧ b", r"\wedge"),
        ("≤", "Partial Order", "Reflexive, antisymmetric, and transitive relation", "a ≤ b", r"\leq"),
        ("⊤", "Top Element", "Greatest element of the lattice (universal set)", "x ≤ ⊤ ∀x", r"\top"),
        ("⊥", "Bottom Element", "Least element of the lattice (empty set)", "⊥ ≤ x ∀x", r"\bot"),
        ("aᶜ", "Complement", "The element that, when joined with a, gives Top, and met with a, gives Bottom", "a ∨ aᶜ = ⊤", r"a^c"),
    ],
    "🌌 General Relativity": [
        ("G_μν", "Einstein Tensor", "Describes curvature of spacetime in Einstein's field equations", "G_μν = 8πG/c⁴ T_μν", r"G_{\mu\nu}"),
        ("T_μν", "Stress-Energy Tensor", "Describes density and flux of energy and momentum in spacetime", "∇_μ T^{μν} = 0", r"T_{\mu\nu}"),
        ("g", "Metric Determinant", "Determinant of the metric tensor, used in volume elements", "dV = √(-g) d⁴x", r"g"),
        ("τ", "Proper Time", "Time measured by a clock following a world line in spacetime", "dτ = √(-g_μν dx^μ dx^ν)", r"\tau"),
        ("R_μν", "Ricci Tensor", "Contraction of the Riemann tensor, used in Einstein's equations", "R_μν = R^α_{μαν}", r"R_{\mu\nu}"),
        ("Λ", "Cosmological Constant", "Energy density of the vacuum of space, causing universal acceleration", "G_μν + Λg_μν = 8πG/c⁴ T_μν", r"\Lambda"),
    ],
    "🌐 Spherical Trigonometry": [
        ("sin(a)/sin(A)", "Law of Sines", "Relates sides and angles of spherical triangles", "sin(a)/sin(A) = sin(b)/sin(B)", r"\frac{\sin a}{\sin A}"),
        ("cos(a)", "Law of Cosines", "Relates sides and angles of spherical triangles", "cos(a) = cos(b)cos(c) + sin(b)sin(c)cos(A)", r"\cos a"),
        ("hav(θ)", "Haversine", "Half of the versine, used in navigation to calculate distances", "hav(θ) = sin²(θ/2)", r"\text{hav}(\theta)"),
        ("versin(θ)", "Versine", "1 minus cosine, historically used in astronomy", "versin(θ) = 1 - cos(θ)", r"\text{versin}(\theta)"),
        ("E", "Spherical Excess", "Amount by which the sum of angles of a spherical triangle exceeds 180°", "Area = R² × E", r"E"),
    ],
    "🎭 Fuzzy Logic": [
        ("μ_A(x)", "Membership Function", "Degree of truth (between 0 and 1) that x belongs to set A", "μ_A(5) = 0.8", r"\mu_A(x)"),
        ("max(μ_A, μ_B)", "Fuzzy Union", "Logical OR in fuzzy logic, taking the maximum membership", "A ∪ B", r"\max(\mu_A, \mu_B)"),
        ("min(μ_A, μ_B)", "Fuzzy Intersection", "Logical AND in fuzzy logic, taking the minimum membership", "A ∩ B", r"\min(\mu_A, \mu_B)"),
        ("1 - μ_A(x)", "Fuzzy Complement", "Logical NOT in fuzzy logic", "¬A", r"1 - \mu_A(x)"),
        ("∼", "Fuzzy Relation", "Mapping between fuzzy sets across different universes", "R = A ∼ B", r"\sim"),
    ]
    # --- NEW CATEGORIES END ---
}

# --- Stylesheets ---
LIGHT_QSS = """
    QMainWindow { background-color: #f4f4f9; }
    QToolBar { background-color: #fff; border-bottom: 1px solid #ccc; spacing: 5px; padding: 4px; }
    QTabWidget::pane { border: 1px solid #ccc; background: #fff; }
    QTabBar::tab { background: #e0e0e0; padding: 8px 12px; border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 2px; font-weight: bold; }
    QTabBar::tab:selected { background: #fff; border-bottom: none; color: #3a7ca5; }
    QTableWidget { gridline-color: #ddd; background-color: #fff; alternate-background-color: #f9f9f9; }
    QTableWidget::item { padding: 8px; }
    QTableWidget::item:hover { background-color: #e0f7fa; }
    QHeaderView::section { background-color: #3a7ca5; color: white; padding: 5px; border: 1px solid #ddd; font-weight: bold; }
    QLineEdit, QComboBox { padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; background: #fff; }
    QPushButton { padding: 6px 10px; border: none; border-radius: 4px; background-color: #3a7ca5; color: white; font-weight: bold; }
    QPushButton:hover { background-color: #2d6285; }
    QPushButton:checked { background-color: #2d6285; }
    QToolButton { padding: 6px 10px; border: none; border-radius: 4px; background-color: #3a7ca5; color: white; font-weight: bold; }
    QToolButton:hover { background-color: #2d6285; }
    QToolButton::menu-arrow { width: 8px; height: 8px; }
    QCheckBox { spacing: 5px; }
    #DetailPanel { background-color: #ffffff; border: 1px solid #ddd; border-radius: 8px; }
    QStatusBar { background-color: #e0e0e0; color: #333; font-weight: bold; }
    QDialog { background-color: #ffffff; }
    QSplitter::handle { background-color: #ccc; }
    QSplitter::handle:vertical { height: 6px; }
"""

DARK_QSS = """
    QMainWindow { background-color: #1e1e2e; }
    QToolBar { background-color: #181825; border-bottom: 1px solid #313244; spacing: 5px; padding: 4px; }
    QTabWidget::pane { border: 1px solid #313244; background: #181825; }
    QTabBar::tab { background: #313244; color: #cdd6f4; padding: 8px 12px; border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 2px; font-weight: bold; }
    QTabBar::tab:selected { background: #181825; border-bottom: none; color: #89b4fa; }
    QTableWidget { gridline-color: #313244; background-color: #181825; alternate-background-color: #1e1e2e; color: #cdd6f4; }
    QTableWidget::item { padding: 8px; }
    QTableWidget::item:hover { background-color: #2a2b3d; }
    QHeaderView::section { background-color: #89b4fa; color: #1e1e2e; padding: 5px; border: 1px solid #313244; font-weight: bold; }
    QLineEdit, QComboBox { padding: 6px; border: 1px solid #45475a; border-radius: 4px; font-size: 14px; background-color: #313244; color: #cdd6f4; }
    QPushButton { padding: 6px 10px; border: none; border-radius: 4px; background-color: #89b4fa; color: #1e1e2e; font-weight: bold; }
    QPushButton:hover { background-color: #b4befe; }
    QPushButton:checked { background-color: #b4befe; }
    QToolButton { padding: 6px 10px; border: none; border-radius: 4px; background-color: #89b4fa; color: #1e1e2e; font-weight: bold; }
    QToolButton:hover { background-color: #b4befe; }
    QToolButton::menu-arrow { width: 8px; height: 8px; }
    QCheckBox { color: #cdd6f4; spacing: 5px; }
    #DetailPanel { background-color: #181825; border: 1px solid #313244; border-radius: 8px; color: #cdd6f4; }
    QStatusBar { background-color: #11111b; color: #a6adc8; font-weight: bold; }
    QDialog { background-color: #181825; color: #cdd6f4; }
    QSplitter::handle { background-color: #313244; }
    QSplitter::handle:vertical { height: 6px; }
"""

class QuickJumpDialog(QDialog):
    """Command Palette style dialog for jumping to symbols instantly"""
    def __init__(self, math_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quick Jump (Ctrl+K)")
        self.resize(400, 300)
        self.math_data = math_data
        self.selected_data = None
        
        layout = QVBoxLayout(self)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Type to search symbols or names...")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.textChanged.connect(self.update_results)
        layout.addWidget(self.search_bar)
        
        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.select_item)
        layout.addWidget(self.results_list)
        
        self.flat_data = []
        for cat, items in math_data.items():
            for item in items:
                self.flat_data.append((cat, item[0], item[1], item[2]))
        
        self.update_results("")
        self.search_bar.setFocus()

    def update_results(self, text):
        text = text.lower().strip()
        self.results_list.clear()
        
        matched_items = []
        for cat, sym, name, desc in self.flat_data:
            if text in sym.lower() or text in name.lower():
                matched_items.append((cat, sym, name, desc))
                
        # Sort results alphabetically by symbol name for better visual scanning
        matched_items.sort(key=lambda x: x[2].lower())
        
        for cat, sym, name, desc in matched_items:
            display_text = f"{sym}  |  {name}  ({cat})"
            item = QListWidgetItem(display_text)
            item.setToolTip(desc)
            item.setData(Qt.UserRole, (cat, sym, name))
            self.results_list.addItem(item)
                
        if self.results_list.count() > 0:
            self.results_list.setCurrentRow(0)

    def select_item(self, item):
        self.selected_data = item.data(Qt.UserRole)
        self.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and self.results_list.currentItem():
            self.select_item(self.results_list.currentItem())
        else:
            super().keyPressEvent(event)


class QuizDialog(QDialog):
    """Dialog for the Flashcard/Quiz Mode"""
    def __init__(self, math_data, high_score, max_streak, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎓 Math Symbols Quiz")
        self.resize(500, 550)
        self.math_data = math_data
        self.score = 0
        self.high_score = high_score
        self.max_streak = max_streak
        self.current_streak = 0
        self.questions_asked = 0
        
        self.all_symbols = []
        for cat, items in math_data.items():
            for item in items:
                self.all_symbols.append((cat, item[0], item[1], item[3]))
                
        self.layout = QVBoxLayout(self)
        
        stats_layout = QHBoxLayout()
        self.score_label = QLabel(f"Score: 0 / 0\nHigh Score: {self.high_score}")
        self.score_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.score_label.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(self.score_label)
        
        self.streak_label = QLabel(f"Streak: 0\nMax Streak: {self.max_streak}")
        self.streak_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.streak_label.setAlignment(Qt.AlignCenter)
        self.streak_label.setStyleSheet("color: orange;")
        stats_layout.addWidget(self.streak_label)
        
        self.time_label = QLabel("Time: --")
        self.time_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("color: red;")
        self.time_label.hide()
        stats_layout.addWidget(self.time_label)
        
        self.layout.addLayout(stats_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 10)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Questions: %v / %m")
        self.layout.addWidget(self.progress_bar)
        
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Quiz Category:"))
        self.cat_combo = QComboBox()
        self.cat_combo.addItem("All Categories")
        for cat in math_data.keys():
            self.cat_combo.addItem(cat)
        self.cat_combo.currentIndexChanged.connect(self.update_quiz_pool)
        filter_layout.addWidget(self.cat_combo)
        
        self.reverse_cb = QCheckBox("Reverse (Guess Sym)")
        self.reverse_cb.stateChanged.connect(self.next_question)
        filter_layout.addWidget(self.reverse_cb)
        
        self.timed_cb = QCheckBox("Timed (15s)")
        self.timed_cb.stateChanged.connect(self.toggle_timer)
        filter_layout.addWidget(self.timed_cb)
        
        self.layout.addLayout(filter_layout)
        
        self.prompt_label = QLabel("What is the name of this symbol?\n(Tip: Press 1-4 to answer, Enter for next)")
        self.prompt_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.prompt_label)
        
        self.symbol_label = QLabel("?")
        self.symbol_label.setFont(QFont("Arial", 48, QFont.Bold))
        self.symbol_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.symbol_label)
        
        self.category_hint_label = QLabel("Category: ???")
        self.category_hint_label.setAlignment(Qt.AlignCenter)
        self.category_hint_label.setStyleSheet("color: gray; font-style: italic;")
        self.layout.addWidget(self.category_hint_label)
        
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.feedback_label.setWordWrap(True)
        self.layout.addWidget(self.feedback_label)
        
        self.buttons = []
        for i in range(4):
            btn = QPushButton()
            btn.clicked.connect(lambda checked, b=btn: self.check_answer(b))
            self.buttons.append(btn)
            self.layout.addWidget(btn)
            
        self.skip_btn = QPushButton("⏭️ Skip Question")
        self.skip_btn.clicked.connect(self.next_question)
        self.layout.addWidget(self.skip_btn)
            
        self.next_btn = QPushButton("➡️ Next Question")
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.hide()
        self.layout.addWidget(self.next_btn)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick_timer)
        self.time_left = 15
        
        for i in range(4):
            shortcut = QShortcut(QKeySequence(str(i+1)), self)
            shortcut.activated.connect(lambda i=i: self.check_answer(self.buttons[i]))
            
        self.next_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.next_shortcut.activated.connect(self.next_question)
        self.next_shortcut_2 = QShortcut(QKeySequence(Qt.Key_Space), self)
        self.next_shortcut_2.activated.connect(self.next_question)
        
        self.update_quiz_pool()

    def toggle_timer(self):
        if self.timed_cb.isChecked():
            self.time_label.show()
        else:
            self.time_label.hide()
            self.timer.stop()
        self.next_question()

    def tick_timer(self):
        self.time_left -= 1
        self.time_label.setText(f"Time: {self.time_left}")
        if self.time_left <= 0:
            self.timer.stop()
            self.times_up()
            
    def times_up(self):
        if not self.next_btn.isHidden():
            return
            
        self.feedback_label.setText("⏱️ Time's up!")
        self.feedback_label.setStyleSheet("color: red;")
        self.current_streak = 0
        
        self.questions_asked += 1
        self.progress_bar.setValue(self.questions_asked % 10)
        
        is_reverse = self.reverse_cb.isChecked()
        correct = self.current_question[1] if is_reverse else self.current_question[2]
        example = self.current_question[3]
        
        self.score_label.setText(f"Score: {self.score} / {self.questions_asked}\nHigh Score: {self.high_score}")
        self.streak_label.setText(f"Streak: {self.current_streak}\nMax Streak: {self.max_streak}")
        
        for b in self.buttons:
            b.hide()
            if b.property("answer") == correct:
                b.setStyleSheet("background-color: green; color: white;")
                b.show()
                
        self.skip_btn.hide()
        self.next_btn.show()
        self.next_shortcut.setEnabled(True)

    def update_quiz_pool(self):
        selected_cat = self.cat_combo.currentText()
        if selected_cat == "All Categories":
            self.active_pool = self.all_symbols
        else:
            self.active_pool = [s for s in self.all_symbols if s[0] == selected_cat]
            
        self.next_question()

    def next_question(self):
        self.feedback_label.setText("")
        self.next_btn.hide()
        self.next_shortcut.setEnabled(False)
        self.skip_btn.show()
        
        if self.timed_cb.isChecked():
            self.time_left = 15
            self.time_label.setText(f"Time: {self.time_left}")
            self.timer.start(1000)
        
        if not self.active_pool:
            self.symbol_label.setText("N/A")
            self.category_hint_label.setText("No symbols in this category")
            for b in self.buttons:
                b.hide()
            self.skip_btn.hide()
            return
            
        self.current_question = random.choice(self.active_pool)
        is_reverse = self.reverse_cb.isChecked()
        
        cat_text = self.current_question[0].split(" ", 1)[1] if " " in self.current_question[0] else self.current_question[0]
        self.category_hint_label.setText(f"Category: {cat_text}")
        
        options = []
        target_attr = 1 if is_reverse else 2
        available_pool = [s for s in self.active_pool if s[target_attr] != self.current_question[target_attr]]
        
        if len(available_pool) >= 3:
            options = random.sample(available_pool, 3)
        else:
            options = available_pool
            
        options.append(self.current_question)
        random.shuffle(options)
        
        num_options = len(options)
        if is_reverse:
            self.prompt_label.setText(f"Which symbol represents this name?\n(Tip: Press 1-{num_options} to answer, Enter for next)")
            self.symbol_label.setText(self.current_question[2])
        else:
            self.prompt_label.setText(f"What is the name of this symbol?\n(Tip: Press 1-{num_options} to answer, Enter for next)")
            self.symbol_label.setText(self.current_question[1])
            
        for i in range(4):
            if i < len(options):
                display_text = options[i][1] if is_reverse else options[i][2]
                self.buttons[i].setText(f"{i+1}. {display_text}")
                self.buttons[i].setProperty("answer", display_text)
                self.buttons[i].setStyleSheet("")
                self.buttons[i].show()
            else:
                self.buttons[i].hide()

    def check_answer(self, btn):
        if not self.skip_btn.isVisible() and not self.next_btn.isHidden():
            return
            
        self.timer.stop()
        selected = btn.property("answer") if btn else None
        is_reverse = self.reverse_cb.isChecked()
        correct = self.current_question[1] if is_reverse else self.current_question[2]
        example = self.current_question[3]
        
        self.questions_asked += 1
        self.progress_bar.setValue(self.questions_asked % 10)
        
        if selected == correct:
            self.score += 1
            self.current_streak += 1
            self.feedback_label.setText(f"✅ Correct! Example: {example}")
            self.feedback_label.setStyleSheet("color: green;")
        else:
            self.current_streak = 0
            self.feedback_label.setText(f"❌ Wrong! It was '{correct}'.\nExample: {example}")
            self.feedback_label.setStyleSheet("color: red;")
            
        if self.score > self.high_score:
            self.high_score = self.score
            if self.parent():
                self.parent().save_high_score(self.high_score)
                
        if self.current_streak > self.max_streak:
            self.max_streak = self.current_streak
            if self.parent():
                self.parent().save_max_streak(self.max_streak)
            
        self.score_label.setText(f"Score: {self.score} / {self.questions_asked}\nHigh Score: {self.high_score}")
        self.streak_label.setText(f"Streak: {self.current_streak}\nMax Streak: {self.max_streak}")
        
        for b in self.buttons:
            b.hide()
            if b.property("answer") == correct:
                b.setStyleSheet("background-color: green; color: white;")
                b.show()
            elif b.property("answer") == selected:
                b.setStyleSheet("background-color: red; color: white;")
                b.show()
                
        self.skip_btn.hide()
        self.next_btn.show()
        self.next_shortcut.setEnabled(True)


class MathSymbolsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mathematical Symbols Master Reference v15.0")
        self.resize(1200, 900)
        
        self.settings = QSettings("MyAppDev", "MathSymbolsApp")
        self.is_dark_mode = self.settings.value("dark_mode", False, type=bool)
        self.font_scale = self.settings.value("font_scale", 1.0, type=float)
        self.is_pinned = self.settings.value("is_pinned", False, type=bool)
        
        loaded_favs = self.settings.value("favorites", [])
        self.favorites = [tuple(f) for f in loaded_favs] if loaded_favs else []
        
        self.recent_views = []
        self.high_score = self.settings.value("high_score", 0, type=int)
        self.max_streak = self.settings.value("max_streak", 0, type=int)
        
        self.current_data_tuple = None
        self._is_updating = False

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.init_toolbar()
        
        self.splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(self.splitter, stretch=1)

        self.init_tabs(self.splitter)
        self.init_detail_panel(self.splitter)
        
        self.splitter.setSizes([600, 250])

        self.apply_theme()
        self.update_detail_fonts()
        self.apply_dynamic_styles()
        
        if self.is_pinned:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.pin_btn.setChecked(True)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status_bar()

        self.search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.search_shortcut.activated.connect(lambda: self.search_bar.setFocus())
        
        self.escape_shortcut = QShortcut(QKeySequence("Escape"), self)
        self.escape_shortcut.activated.connect(self.clear_search)
        
        self.copy_latex_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        self.copy_latex_shortcut.activated.connect(self.copy_latex_from_detail)
        
        self.quick_jump_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        self.quick_jump_shortcut.activated.connect(self.open_quick_jump)

        # Restore Window Geometry and Splitter State
        if self.settings.value("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        if self.settings.value("window_state"):
            self.restoreState(self.settings.value("window_state"))
        if self.settings.value("splitter_state"):
            self.splitter.restoreState(self.settings.value("splitter_state"))

        self.tabs.setCurrentIndex(3)  # Start on the first actual category
        self.last_visited_tab = 3

    def update_status_bar(self, custom_msg=None):
        total_symbols = sum(len(syms) for syms in MATH_DATA.values())
        fav_count = len(self.favorites)
        cat_count = len(MATH_DATA)
        idx = self.tabs.currentIndex() if hasattr(self, 'tabs') else -1
        current_cat = "N/A"
        if idx >= 0:
            tab_text = self.tabs.tabText(idx)
            if " (" in tab_text:
                current_cat = tab_text.rsplit(' (', 1)[0]
            else:
                current_cat = tab_text
                
        if custom_msg:
            self.status_bar.showMessage(custom_msg)
        else:
            self.status_bar.showMessage(f"Total Symbols: {total_symbols} | Categories: {cat_count} | Current: {current_cat} | Favorites: {fav_count} | Ready")

    def init_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        toolbar.addWidget(QLabel(" Jump to: "))
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(list(MATH_DATA.keys()))
        self.cat_combo.currentIndexChanged.connect(self.jump_to_category)
        toolbar.addWidget(self.cat_combo)

        toolbar.addSeparator()

        toolbar.addWidget(QLabel(" Search: "))
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search... (Ctrl+F)")
        self.search_bar.setFixedWidth(200)
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.textChanged.connect(self.perform_global_search)
        toolbar.addWidget(self.search_bar)
        
        self.search_filter_cb = QCheckBox("Name/Sym Only")
        toolbar.addWidget(self.search_filter_cb)

        toolbar.addSeparator()
        
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(empty)

        self.pin_btn = QPushButton("📌 Pin")
        self.pin_btn.setCheckable(True)
        self.pin_btn.setChecked(self.is_pinned)
        self.pin_btn.toggled.connect(self.toggle_always_on_top)
        self.pin_btn.setToolTip("Keep window always on top of other applications.")
        toolbar.addWidget(self.pin_btn)

        random_btn = QPushButton("🎲 Random")
        random_btn.clicked.connect(self.go_to_random_symbol)
        toolbar.addWidget(random_btn)

        self.view_btn = QToolButton()
        self.view_btn.setText("⚙️ View")
        self.view_btn.setPopupMode(QToolButton.InstantPopup)
        view_menu = QMenu(self)
        
        self.col_actions = []
        col_names = ["Symbol", "Name", "Description", "Example", "LaTeX"]
        saved_col_states = self.settings.value("col_visibility", [True, True, True, True, True])
        
        for i, name in enumerate(col_names):
            checked = saved_col_states[i] if saved_col_states and i < len(saved_col_states) else True
            act = QAction(name, self, checkable=True, checked=checked)
            act.triggered.connect(lambda checked, idx=i: self.toggle_column(idx, checked))
            view_menu.addAction(act)
            self.col_actions.append(act)
            
        self.view_btn.setMenu(view_menu)
        toolbar.addWidget(self.view_btn)
        
        self.font_btn = QToolButton()
        self.font_btn.setText("A Font")
        self.font_btn.setPopupMode(QToolButton.InstantPopup)
        font_menu = QMenu(self)
        
        font_up_act = QAction("Increase (+10%)", self)
        font_up_act.triggered.connect(lambda: self.adjust_font_scale(0.1))
        font_menu.addAction(font_up_act)
        
        font_down_act = QAction("Decrease (-10%)", self)
        font_down_act.triggered.connect(lambda: self.adjust_font_scale(-0.1))
        font_menu.addAction(font_down_act)
        
        font_reset_act = QAction("Reset (100%)", self)
        font_reset_act.triggered.connect(self.reset_font_scale)
        font_menu.addAction(font_reset_act)
        
        self.font_btn.setMenu(font_menu)
        toolbar.addWidget(self.font_btn)

        self.quiz_btn = QPushButton("🎓 Quiz")
        self.quiz_btn.clicked.connect(self.open_quiz)
        toolbar.addWidget(self.quiz_btn)

        self.export_btn = QPushButton("📤 Export")
        self.export_btn.clicked.connect(self.export_data)
        toolbar.addWidget(self.export_btn)
        
        about_btn = QPushButton("ℹ️ About")
        about_btn.clicked.connect(self.show_about_dialog)
        toolbar.addWidget(about_btn)

        self.theme_btn = QPushButton("☀️ Light Mode" if self.is_dark_mode else "🌙 Dark Mode")
        self.theme_btn.clicked.connect(self.toggle_theme)
        toolbar.addWidget(self.theme_btn)

    def toggle_always_on_top(self, checked):
        self.is_pinned = checked
        self.settings.setValue("is_pinned", checked)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, checked)
        self.show() # Required to apply window flags immediately

    def toggle_column(self, idx, state):
        for i in range(self.tabs.count()):
            table = self.tabs.widget(i).findChild(QTableWidget)
            if table:
                table.setColumnHidden(idx, not state)
        # Save column visibility state
        self.settings.setValue("col_visibility", [act.isChecked() for act in self.col_actions])
                
    def reset_font_scale(self):
        self.font_scale = 1.0
        self.settings.setValue("font_scale", self.font_scale)
        self.update_status_bar(custom_msg="Font scale reset to 100%")
        self.adjust_font_scale(0)

    def init_tabs(self, parent_widget):
        self.tabs = QTabWidget()
        parent_widget.addWidget(self.tabs)
        self.tab_indices = {}
        self.init_special_tabs()
        for category, symbols in MATH_DATA.items():
            self.create_tab(category, symbols)
        self.tabs.currentChanged.connect(self.on_tab_changed)

    def init_detail_panel(self, parent_widget):
        self.detail_panel = QWidget()
        self.detail_panel.setObjectName("DetailPanel")
        
        layout = QHBoxLayout(self.detail_panel)
        layout.setContentsMargins(20, 20, 20, 20)

        self.detail_symbol = QLabel("Select a symbol")
        self.detail_symbol.setAlignment(Qt.AlignCenter)
        self.detail_symbol.setFixedWidth(120)
        layout.addWidget(self.detail_symbol)

        info_layout = QVBoxLayout()
        
        self.detail_name = QLabel("")
        info_layout.addWidget(self.detail_name)
        
        self.detail_category = QLabel("")
        info_layout.addWidget(self.detail_category)

        self.detail_desc = QLabel("")
        self.detail_desc.setWordWrap(True)
        info_layout.addWidget(self.detail_desc)

        self.detail_example = QLabel("")
        info_layout.addWidget(self.detail_example)

        self.detail_latex = QLabel("")
        info_layout.addWidget(self.detail_latex)

        btn_layout = QHBoxLayout()
        
        self.copy_sym_btn = QPushButton("Copy Symbol")
        self.copy_sym_btn.clicked.connect(lambda: self.copy_to_clipboard(self.detail_symbol.text(), "Symbol"))
        btn_layout.addWidget(self.copy_sym_btn)
        
        self.copy_name_btn = QPushButton("Copy Name")
        self.copy_name_btn.clicked.connect(self.copy_name_from_detail)
        btn_layout.addWidget(self.copy_name_btn)
        
        self.copy_latex_btn = QPushButton("Copy LaTeX (Ctrl+E)")
        self.copy_latex_btn.clicked.connect(self.copy_latex_from_detail)
        btn_layout.addWidget(self.copy_latex_btn)
        
        self.copy_ex_btn = QPushButton("Copy Example")
        self.copy_ex_btn.clicked.connect(self.copy_example_from_detail)
        btn_layout.addWidget(self.copy_ex_btn)
        
        self.fav_toggle_btn = QPushButton("❤️ Add to Favorites")
        self.fav_toggle_btn.clicked.connect(self.toggle_favorite_from_detail)
        btn_layout.addWidget(self.fav_toggle_btn)
        
        info_layout.addLayout(btn_layout)

        self.web_search_btn = QPushButton("🔎 Search Web for Symbol")
        self.web_search_btn.clicked.connect(self.search_web_for_symbol)
        info_layout.addWidget(self.web_search_btn)

        layout.addLayout(info_layout, stretch=1)
        parent_widget.addWidget(self.detail_panel)

    def init_special_tabs(self):
        self.fav_table = self.create_table()
        fav_tab = QWidget()
        layout = QVBoxLayout(fav_tab)
        
        clear_fav_btn = QPushButton("🗑️ Clear All Favorites")
        clear_fav_btn.clicked.connect(self.clear_favorites)
        layout.addWidget(clear_fav_btn)
        
        layout.addWidget(self.fav_table)
        fav_idx = self.tabs.addTab(fav_tab, "⭐ Favorites (0)")
        self.tab_indices["Favorites"] = fav_idx
        
        self.recent_table = self.create_table()
        recent_tab = QWidget()
        layout2 = QVBoxLayout(recent_tab)
        
        clear_btn = QPushButton("🗑️ Clear Recent History")
        clear_btn.clicked.connect(self.clear_recent_history)
        layout2.addWidget(clear_btn)
        
        layout2.addWidget(self.recent_table)
        rec_idx = self.tabs.addTab(recent_tab, "⏱️ Recent (0)")
        self.tab_indices["Recent"] = rec_idx
        
        self.update_favorites_table()

        self.search_table = self.create_table()
        search_tab = QWidget()
        layout3 = QVBoxLayout(search_tab)
        layout3.addWidget(self.search_table)
        self.search_tab_index = self.tabs.addTab(search_tab, "🔍 Search Results")
        self.tabs.setTabVisible(self.search_tab_index, False)

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Symbol", "Name", "Description", "Example", "LaTeX"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True) 
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.show_context_menu)
        table.itemSelectionChanged.connect(lambda t=table: self.update_detail_panel(t))
        table.doubleClicked.connect(lambda idx, t=table: self.copy_latex_from_table(t, idx))
        
        for i, act in enumerate(self.col_actions):
            table.setColumnHidden(i, not act.isChecked())
            
        return table

    def populate_table(self, table, data):
        # Preserve user's sort selection
        sort_col = table.horizontalHeader().sortIndicatorSection()
        sort_order = table.horizontalHeader().sortIndicatorOrder()
        
        table.setSortingEnabled(False)
        table.setRowCount(len(data))
        
        base_sym = int(16 * self.font_scale)
        base_txt = int(11 * self.font_scale)
        
        for row, item_data in enumerate(data):
            sym, name, desc, ex, latex = item_data
            
            sym_item = QTableWidgetItem(sym)
            sym_item.setTextAlignment(Qt.AlignCenter)
            sym_item.setFont(QFont("Arial", base_sym, QFont.Bold))
            sym_item.setToolTip(f"{name}: {desc}\n(Double-click row to copy LaTeX)")
            
            if item_data in self.favorites:
                sym_item.setForeground(Qt.gold)
            
            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("Arial", base_txt, QFont.Bold))
            name_item.setTextAlignment(Qt.AlignCenter)
            name_item.setToolTip(desc)

            desc_item = QTableWidgetItem(desc)
            desc_item.setFont(QFont("Arial", base_txt))
            
            ex_item = QTableWidgetItem(ex)
            ex_item.setTextAlignment(Qt.AlignCenter)
            ex_item.setFont(QFont("Courier New", base_txt))

            latex_item = QTableWidgetItem(latex)
            latex_item.setTextAlignment(Qt.AlignCenter)
            latex_item.setFont(QFont("Courier New", base_txt, QFont.Bold))
            
            latex_color = Qt.green if self.is_dark_mode else Qt.darkGreen
            latex_item.setForeground(latex_color)

            table.setItem(row, 0, sym_item)
            table.setItem(row, 1, name_item)
            table.setItem(row, 2, desc_item)
            table.setItem(row, 3, ex_item)
            table.setItem(row, 4, latex_item)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Interactive)
        header.setSectionResizeMode(4, QHeaderView.Interactive)
        
        table.setSortingEnabled(True)
        # Reapply sort if valid, otherwise default
        if sort_col >= 0:
            table.sortByColumn(sort_col, sort_order)
        else:
            table.sortByColumn(1, Qt.AscendingOrder)

    def create_tab(self, category, symbols):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        table = self.create_table()
        self.populate_table(table, symbols)
        layout.addWidget(table)
        idx = self.tabs.addTab(tab, f"{category} ({len(symbols)})")
        self.tab_indices[category] = idx

    def jump_to_category(self, index):
        cat_name = list(MATH_DATA.keys())[index]
        if cat_name in self.tab_indices:
            self.tabs.setCurrentIndex(self.tab_indices[cat_name])

    def go_to_random_symbol(self):
        cat_name = random.choice(list(MATH_DATA.keys()))
        symbols = MATH_DATA[cat_name]
        rand_sym = random.choice(symbols)
        
        if cat_name in self.tab_indices:
            self.tabs.setCurrentIndex(self.tab_indices[cat_name])
            table = self.tabs.widget(self.tab_indices[cat_name]).findChild(QTableWidget)
            if table:
                items = table.findItems(rand_sym[0], Qt.MatchExactly)
                if items:
                    row = items[0].row()
                    table.selectRow(row)
                    table.scrollToItem(items[0], QTableWidget.PositionAtCenter)

    def open_quick_jump(self):
        dialog = QuickJumpDialog(MATH_DATA, self)
        if dialog.exec() == QDialog.Accepted and dialog.selected_data:
            cat_name, sym, name = dialog.selected_data
            if cat_name in self.tab_indices:
                self.tabs.setCurrentIndex(self.tab_indices[cat_name])
                table = self.tabs.widget(self.tab_indices[cat_name]).findChild(QTableWidget)
                if table:
                    items = table.findItems(sym, Qt.MatchExactly)
                    if items:
                        row = items[0].row()
                        table.selectRow(row)
                        table.scrollToItem(items[0], QTableWidget.PositionAtCenter)

    def perform_global_search(self, text):
        text = text.lower().strip()
        if not text:
            self.clear_search()
            return

        results = []
        name_sym_only = self.search_filter_cb.isChecked()
        
        for category, symbols in MATH_DATA.items():
            for sym_tuple in symbols:
                fields = [sym_tuple[0], sym_tuple[1]] if name_sym_only else sym_tuple
                if any(text in str(field).lower() for field in fields):
                    results.append(sym_tuple)

        self.populate_table(self.search_table, results)
        self.tabs.setTabText(self.search_tab_index, f"🔍 Search Results ({len(results)})")
        self.tabs.setTabVisible(self.search_tab_index, True)
        
        if self.tabs.currentIndex() != self.search_tab_index:
            self.last_visited_tab = self.tabs.currentIndex()
            self.tabs.setCurrentIndex(self.search_tab_index)
            
        self.update_status_bar(custom_msg=f"Found {len(results)} symbols matching '{text}'.")

    def clear_search(self):
        if self.search_bar.text():
            self.search_bar.clear()
            
        if self.tabs.isTabVisible(self.search_tab_index):
            self.tabs.setTabVisible(self.search_tab_index, False)
            self.tabs.setTabText(self.search_tab_index, "🔍 Search Results")
            self.tabs.setCurrentIndex(self.last_visited_tab)
            
        self.update_status_bar()

    def refresh_table_by_index(self, idx):
        """Helper to refresh tables safely without causing signal loops or losing selection."""
        table = self.tabs.widget(idx).findChild(QTableWidget)
        if not table: return
        
        selected_sym = ""
        selected_name = ""
        current_row = table.currentRow()
        if current_row >= 0 and table.item(current_row, 0) and table.item(current_row, 1):
            selected_sym = table.item(current_row, 0).text()
            selected_name = table.item(current_row, 1).text()

        if idx == self.tab_indices["Favorites"]:
            data = self.favorites
        elif idx == self.tab_indices["Recent"]:
            data = self.recent_views
        elif idx == self.search_tab_index:
            data = []
            for row in range(table.rowCount()):
                data.append((
                    table.item(row, 0).text(),
                    table.item(row, 1).text(),
                    table.item(row, 2).text(),
                    table.item(row, 3).text(),
                    table.item(row, 4).text()
                ))
        else:
            cat_name = self.tabs.tabText(idx).rsplit(' (', 1)[0]
            data = MATH_DATA.get(cat_name, [])
            
        table.blockSignals(True)
        self.populate_table(table, data)
        
        if selected_sym:
            items = table.findItems(selected_sym, Qt.MatchExactly)
            found = False
            for item in items:
                if item.column() == 0 and table.item(item.row(), 1).text() == selected_name:
                    table.selectRow(item.row())
                    table.scrollToItem(item, QTableWidget.PositionAtCenter)
                    found = True
                    break
            if not found and table.rowCount() > 0:
                table.selectRow(0)
                
        table.blockSignals(False)
        
        if self.tabs.currentIndex() == idx and not self._is_updating:
            self.update_detail_panel(table)

    def update_favorites_table(self):
        if self.tabs.currentIndex() == self.tab_indices["Favorites"] and not self._is_updating:
            self.refresh_table_by_index(self.tab_indices["Favorites"])
        else:
            self.populate_table(self.fav_table, self.favorites)
        self.tabs.setTabText(self.tab_indices["Favorites"], f"⭐ Favorites ({len(self.favorites)})")
        self.update_status_bar()

    def update_recent_table(self):
        if self.tabs.currentIndex() == self.tab_indices["Recent"] and not self._is_updating:
            self.refresh_table_by_index(self.tab_indices["Recent"])
        else:
            self.populate_table(self.recent_table, self.recent_views)
        self.tabs.setTabText(self.tab_indices["Recent"], f"⏱️ Recent ({len(self.recent_views)})")
        
    def clear_recent_history(self):
        self.recent_views.clear()
        self.update_recent_table()
        self.update_status_bar(custom_msg="Recent history cleared.")
        
    def clear_favorites(self):
        self.favorites.clear()
        self.save_favorites()
        self.update_favorites_table()
        self.refresh_table_by_index(self.tabs.currentIndex())
        self.update_status_bar(custom_msg="Favorites cleared.")

    def on_tab_changed(self, index):
        if index != self.search_tab_index and self.tabs.isTabVisible(self.search_tab_index):
            self.search_bar.clear()
            self.tabs.setTabVisible(self.search_tab_index, False)
            
        if index != self.search_tab_index and index != self.tab_indices["Favorites"] and index != self.tab_indices["Recent"]:
            self.last_visited_tab = index
            
        current_table = self.tabs.currentWidget().findChild(QTableWidget) if self.tabs.currentWidget() else None
        if current_table:
            current_table.clearSelection()
            
        self.detail_symbol.setText("Select a symbol")
        self.detail_name.setText("")
        self.detail_category.setText("")
        self.detail_desc.setText("")
        self.detail_example.setText("")
        self.detail_latex.setText("")
        self.fav_toggle_btn.setText("❤️ Add to Favorites")
        self.fav_toggle_btn.setEnabled(False)
        self.current_data_tuple = None
        
        self.update_status_bar()

    def find_category_for_symbol(self, data_tuple):
        for cat, syms in MATH_DATA.items():
            if data_tuple in syms:
                return cat
        for cat, syms in MATH_DATA.items():
            for s in syms:
                if s[0] == data_tuple[0] and s[1] == data_tuple[1]:
                    return cat
        return "Unknown"

    def update_detail_panel(self, table):
        self._is_updating = True
        selected_items = table.selectedItems()
        if not selected_items:
            self.detail_symbol.setText("Select a symbol")
            self.detail_name.setText("")
            self.detail_category.setText("")
            self.detail_desc.setText("")
            self.detail_example.setText("")
            self.detail_latex.setText("")
            self.fav_toggle_btn.setText("❤️ Add to Favorites")
            self.fav_toggle_btn.setEnabled(False)
            self.current_data_tuple = None
            self._is_updating = False
            return
        
        row = selected_items[0].row()
        data_tuple = (
            table.item(row, 0).text(),
            table.item(row, 1).text(),
            table.item(row, 2).text(),
            table.item(row, 3).text(),
            table.item(row, 4).text()
        )
        self.current_data_tuple = data_tuple

        self.detail_symbol.setText(data_tuple[0])
        self.detail_name.setText(data_tuple[1])
        
        category = self.find_category_for_symbol(data_tuple)
        self.detail_category.setText(f"Category: {category}")
        
        self.detail_desc.setText(f"Description: {data_tuple[2]}")
        self.detail_example.setText(f"Example: {data_tuple[3]}")
        self.detail_latex.setText(f"LaTeX: {data_tuple[4]}")
        
        self.fav_toggle_btn.setEnabled(True)
        if data_tuple in self.favorites:
            self.fav_toggle_btn.setText("❌ Remove from Favorites")
        else:
            self.fav_toggle_btn.setText("❤️ Add to Favorites")

        if data_tuple in self.recent_views:
            self.recent_views.remove(data_tuple)
        self.recent_views.insert(0, data_tuple)
        if len(self.recent_views) > 15:
            self.recent_views.pop()
        
        self.update_recent_table()
        self._is_updating = False

    def show_context_menu(self, pos: QPoint):
        table = self.sender()
        item = table.itemAt(pos)
        if not item:
            return

        row = item.row()
        data_tuple = (
            table.item(row, 0).text(),
            table.item(row, 1).text(),
            table.item(row, 2).text(),
            table.item(row, 3).text(),
            table.item(row, 4).text()
        )

        menu = QMenu(self)

        copy_sym_action = QAction(f"Copy Symbol: {data_tuple[0]}", self)
        copy_sym_action.triggered.connect(lambda checked, d=data_tuple: self.copy_to_clipboard(d[0], "Symbol"))
        
        copy_name_action = QAction(f"Copy Name: {data_tuple[1]}", self)
        copy_name_action.triggered.connect(lambda checked, d=data_tuple: self.copy_to_clipboard(d[1], "Name"))
        
        copy_latex_action = QAction(f"Copy LaTeX: {data_tuple[4]}", self)
        copy_latex_action.triggered.connect(lambda checked, d=data_tuple: self.copy_to_clipboard(d[4], "LaTeX"))
        
        copy_ex_action = QAction(f"Copy Example: {data_tuple[3]}", self)
        copy_ex_action.triggered.connect(lambda checked, d=data_tuple: self.copy_to_clipboard(d[3], "Example"))

        copy_row_action = QAction("Copy Formatted Row", self)
        copy_row_action.triggered.connect(lambda checked, d=data_tuple: self.copy_formatted_row(d))
        
        copy_md_action = QAction("Copy as Markdown Row", self)
        copy_md_action.triggered.connect(lambda checked, d=data_tuple: self.copy_markdown_row(d))

        web_search_action = QAction("🔎 Search Web", self)
        web_search_action.triggered.connect(lambda checked, d=data_tuple: self.search_web_for_name(d[1]))

        menu.addAction(copy_sym_action)
        menu.addAction(copy_name_action)
        menu.addAction(copy_latex_action)
        menu.addAction(copy_ex_action)
        menu.addAction(copy_row_action)
        menu.addAction(copy_md_action)
        menu.addSeparator()
        menu.addAction(web_search_action)
        menu.addSeparator()

        is_fav_tab = (table == self.fav_table)
        
        if not is_fav_tab:
            add_fav_action = QAction("⭐ Add to Favorites", self)
            add_fav_action.triggered.connect(lambda checked, d=data_tuple: self.add_favorite(d))
            menu.addAction(add_fav_action)
        else:
            rem_fav_action = QAction("❌ Remove from Favorites", self)
            rem_fav_action.triggered.connect(lambda checked, d=data_tuple: self.remove_favorite(d))
            menu.addAction(rem_fav_action)

        menu.exec(table.viewport().mapToGlobal(pos))

    def copy_latex_from_table(self, table, index):
        row = index.row()
        latex = table.item(row, 4).text()
        self.copy_to_clipboard(latex, "LaTeX")

    def copy_latex_from_detail(self):
        if self.current_data_tuple:
            latex = self.current_data_tuple[4]
            self.copy_to_clipboard(latex, "LaTeX")
            
    def copy_name_from_detail(self):
        if self.current_data_tuple:
            name = self.current_data_tuple[1]
            self.copy_to_clipboard(name, "Name")

    def copy_example_from_detail(self):
        if self.current_data_tuple:
            ex = self.current_data_tuple[3]
            self.copy_to_clipboard(ex, "Example")

    def copy_to_clipboard(self, text, item_type):
        QApplication.clipboard().setText(text)
        self.update_status_bar(custom_msg=f"Copied {item_type}: '{text}' to clipboard!")

    def copy_formatted_row(self, data_tuple):
        sym, name, desc, ex, latex = data_tuple
        text = f"Symbol: {sym}\nName: {name}\nDescription: {desc}\nExample: {ex}\nLaTeX: {latex}"
        QApplication.clipboard().setText(text)
        self.update_status_bar(custom_msg="Copied formatted row to clipboard!")
        
    def copy_markdown_row(self, data_tuple):
        sym, name, desc, ex, latex = data_tuple
        desc_md = desc.replace('|', '\\|')
        text = f"| `{sym}` | **{name}** | {desc_md} | `{ex}` | `{latex}` |"
        QApplication.clipboard().setText(text)
        self.update_status_bar(custom_msg="Copied Markdown row to clipboard!")

    def toggle_favorite_from_detail(self):
        if not self.current_data_tuple:
            return
        data_tuple = self.current_data_tuple
        
        if data_tuple in self.favorites:
            self.remove_favorite(data_tuple)
            self.fav_toggle_btn.setText("❤️ Add to Favorites")
        else:
            self.add_favorite(data_tuple)
            self.fav_toggle_btn.setText("❌ Remove from Favorites")

    def add_favorite(self, data_tuple):
        if data_tuple not in self.favorites:
            self.favorites.append(data_tuple)
            self.save_favorites()
            self.update_favorites_table()
            self.update_status_bar(custom_msg=f"Added '{data_tuple[1]}' to favorites.")
            self.refresh_table_by_index(self.tabs.currentIndex())

    def remove_favorite(self, data_tuple):
        if data_tuple in self.favorites:
            self.favorites.remove(data_tuple)
            self.save_favorites()
            self.update_favorites_table()
            self.update_status_bar(custom_msg=f"Removed '{data_tuple[1]}' from favorites.")
            if self.tabs.currentIndex() == self.tab_indices["Favorites"]:
                self.fav_toggle_btn.setText("❤️ Add to Favorites")
            self.refresh_table_by_index(self.tabs.currentIndex())

    def save_favorites(self):
        self.settings.setValue("favorites", [list(f) for f in self.favorites])

    def save_high_score(self, score):
        self.high_score = score
        self.settings.setValue("high_score", score)
        
    def save_max_streak(self, streak):
        self.max_streak = streak
        self.settings.setValue("max_streak", streak)

    def export_data(self):
        items = ["Favorites", "Current Category", "All Symbols"]
        choice, ok = QInputDialog.getItem(self, "Export Data", "What would you like to export?", items, 0, False)
        
        if not ok:
            return
            
        data_to_export = []
        if choice == "Favorites":
            if not self.favorites:
                self.update_status_bar(custom_msg="No favorites to export!")
                return
            data_to_export = self.favorites
        elif choice == "Current Category":
            idx = self.tabs.currentIndex()
            if idx == self.tab_indices["Favorites"]:
                data_to_export = self.favorites
            elif idx == self.tab_indices["Recent"]:
                data_to_export = self.recent_views
            elif idx == self.search_tab_index:
                table = self.tabs.widget(idx).findChild(QTableWidget)
                for row in range(table.rowCount()):
                    data_to_export.append((
                        table.item(row, 0).text(),
                        table.item(row, 1).text(),
                        table.item(row, 2).text(),
                        table.item(row, 3).text(),
                        table.item(row, 4).text()
                    ))
            else:
                cat_name = self.tabs.tabText(idx).rsplit(' (', 1)[0]
                data_to_export = MATH_DATA.get(cat_name, [])
                
            if not data_to_export:
                self.update_status_bar(custom_msg="No category selected or data is empty!")
                return
        else:
            data_to_export = [sym for cat_syms in MATH_DATA.values() for sym in cat_syms]
            
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, f"Export {choice}", f"math_{choice.lower().replace(' ', '_')}", "LaTeX (*.tex);;Anki CSV (*.csv);;JSON (*.json);;HTML (*.html);;Markdown (*.md);;CSV (*.csv);;Text (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    if file_path.endswith('.csv'):
                        writer = csv.writer(f)
                        writer.writerow(["Symbol", "Name", "Description", "Example", "LaTeX"])
                        for row in data_to_export:
                            writer.writerow(row)
                    elif file_path.endswith('.md'):
                        f.write(f"# Mathematical Symbols: {choice}\n\n")
                        f.write("| Symbol | Name | Description | Example | LaTeX |\n|---|---|---|---|---|\n")
                        for sym, name, desc, ex, latex in data_to_export:
                            desc_md = desc.replace('|', '\\|')
                            f.write(f"| `{sym}` | **{name}** | {desc_md} | `{ex}` | `{latex}` |\n")
                    elif file_path.endswith('.html'):
                        f.write("<!DOCTYPE html>\n<html>\n<head>\n<style>body{font-family:sans-serif;} table{border-collapse:collapse;width:100%;} th,td{border:1px solid #ddd;padding:8px;} th{background-color:#f2f2f2;}</style>\n</head>\n<body>\n")
                        f.write(f"<h1>Mathematical Symbols: {html.escape(choice)}</h1>\n<table>\n<tr><th>Symbol</th><th>Name</th><th>Description</th><th>Example</th><th>LaTeX</th></tr>\n")
                        for sym, name, desc, ex, latex in data_to_export:
                            f.write(f"<tr><td style='text-align:center;font-size:1.2em;font-weight:bold;'>{html.escape(sym)}</td><td>{html.escape(name)}</td><td>{html.escape(desc)}</td><td>{html.escape(ex)}</td><td><code>{html.escape(latex)}</code></td></tr>\n")
                        f.write("</table>\n</body>\n</html>")
                    elif file_path.endswith('.tex'):
                        f.write(r"\documentclass{article}" + "\n")
                        f.write(r"\usepackage{amsmath, amssymb}" + "\n")
                        f.write(r"\title{Mathematical Symbols: " + choice + "}\n")
                        f.write(r"\begin{document}" + "\n")
                        f.write(r"\maketitle" + "\n")
                        f.write(r"\begin{itemize}" + "\n")
                        for sym, name, desc, ex, latex in data_to_export:
                            f.write(r"\item \textbf{" + name + r"} ($" + latex + r"$): " + desc + r" (e.g., $ " + ex + r" $)" + "\n")
                        f.write(r"\end{itemize}" + "\n")
                        f.write(r"\end{document}" + "\n")
                    elif file_path.endswith('.json'):
                        keys = ["symbol", "name", "description", "example", "latex"]
                        json_data = [dict(zip(keys, d)) for d in data_to_export]
                        json.dump(json_data, f, indent=4)
                    else:
                        for sym, name, desc, ex, latex in data_to_export:
                            f.write(f"{sym} | {name} | {desc} | {ex} | {latex}\n")
                            
                self.update_status_bar(custom_msg=f"Successfully exported {choice} to {file_path}")
            except Exception as e:
                self.update_status_bar(custom_msg=f"Error saving file: {e}")

    def update_detail_fonts(self):
        self.detail_symbol.setFont(QFont("Arial", int(36 * self.font_scale), QFont.Bold))
        self.detail_name.setFont(QFont("Arial", int(16 * self.font_scale), QFont.Bold))
        self.detail_category.setFont(QFont("Arial", int(10 * self.font_scale), QFont.Bold))
        self.detail_desc.setFont(QFont("Arial", int(11 * self.font_scale)))
        self.detail_example.setFont(QFont("Courier New", int(12 * self.font_scale), QFont.Bold))
        self.detail_latex.setFont(QFont("Courier New", int(12 * self.font_scale)))

    def adjust_font_scale(self, delta):
        new_scale = round(self.font_scale + delta, 1)
        if delta == 0:
            new_scale = 1.0
            self.font_scale = 1.0
            
        if 0.7 <= new_scale <= 2.0:
            self.font_scale = new_scale
            self.settings.setValue("font_scale", self.font_scale)
            self.update_status_bar(custom_msg=f"Font scale set to {int(self.font_scale*100)}%")
            
            self.update_detail_fonts()
            
            for i in range(self.tabs.count()):
                if not self.tabs.isTabVisible(i) and i != self.search_tab_index:
                    continue
                self.refresh_table_by_index(i)

    def open_quiz(self):
        self.quiz_dialog = QuizDialog(MATH_DATA, self.high_score, self.max_streak, self)
        self.quiz_dialog.exec()

    def search_web_for_symbol(self):
        if not self.current_data_tuple:
            return
        self.search_web_for_name(self.current_data_tuple[1])
        
    def search_web_for_name(self, name):
        search_term = f"{name} mathematics symbol"
        url = QUrl(f"https://www.google.com/search?q={search_term}")
        QDesktopServices.openUrl(url)
        self.update_status_bar(custom_msg=f"Opening browser for '{search_term}'...")

    def show_about_dialog(self):
        total_symbols = sum(len(syms) for syms in MATH_DATA.values())
        total_categories = len(MATH_DATA)
        QMessageBox.about(self, "About Math Symbols Master",
            f"<h3>Mathematical Symbols Master Reference v15.0</h3>"
            f"<p>A comprehensive reference and study tool for mathematical symbols and notation.</p>"
            f"<p><b>Categories:</b> {total_categories}</p>"
            f"<p><b>Total Symbols:</b> {total_symbols}</p>"
            f"<p>Features: Dark Mode, Global Search, Quick Jump (Ctrl+K), Always on Top Pin, Timed Quizzes, Multi-Format Exports, State Persistence, and more!</p>"
            f"<p>Built with PySide6.</p>")

    def apply_dynamic_styles(self):
        gray_color = "#888888" if not self.is_dark_mode else "#a6adc8"
        self.detail_category.setStyleSheet(f"color: {gray_color};")

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.settings.setValue("dark_mode", self.is_dark_mode)
        self.theme_btn.setText("☀️ Light Mode" if self.is_dark_mode else "🌙 Dark Mode")
        self.apply_theme()
        self.apply_dynamic_styles()
        for i in range(self.tabs.count()):
            self.refresh_table_by_index(i)

    def apply_theme(self):
        self.setStyleSheet(DARK_QSS if self.is_dark_mode else LIGHT_QSS)

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("window_state", self.saveState())
        self.settings.setValue("splitter_state", self.splitter.saveState())
        self.settings.sync()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MathSymbolsApp()
    window.show()
    sys.exit(app.exec())