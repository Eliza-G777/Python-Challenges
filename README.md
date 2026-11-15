# Physics, Math and Engineering Projects in Python

Ten short projects that use Python to answer real questions in physics, mathematics and engineering. Each one is a single file with clear comments, prints its results and saves a chart.

### Physics

| # | Project | Question |
| --- | --- | --- |
| 01 | [Projectile Motion With Air Resistance](physics/01-projectile-motion) | How far does a launched ball travel, and how much does air resistance change the distance and the best launch angle? |
| 02 | [When the Pendulum Formula Breaks](physics/02-pendulum) | The school formula T = 2π√(L/g) assumes small swings. How wrong is it for big swings? |
| 03 | [Earth's Orbit From Newton's Law of Gravity](physics/03-earth-orbit) | Knowing only Newton's law of gravity and Earth's distance and speed, can a computer predict the length of a year? |

### Mathematics

| # | Project | Question |
| --- | --- | --- |
| 04 | [Estimating π With Random Darts](math/04-monte-carlo-pi) | Can random numbers calculate π? And how fast does the answer improve as we use more of them? |
| 05 | [Exploring Prime Numbers](math/05-primes) | How are primes spread out, and does Goldbach's conjecture hold for the numbers we can check? |
| 06 | [Solving Equations: Newton's Method vs Bisection](math/06-newtons-method) | How can a computer solve an equation like x³ − 2x − 5 = 0, and why is Newton's method so much faster than halving an interval? |

### Engineering

| # | Project | Question |
| --- | --- | --- |
| 07 | [Charging a Capacitor: The RC Circuit](engineering/07-rc-circuit) | How long does a capacitor take to charge through a resistor, and why do engineers say it's full after 5 time constants? |
| 08 | [Designing a Footbridge Beam](engineering/08-beam-bending) | Which material makes the stiffest 4 m footbridge beam, and why do real bridges use I-shaped beams? |
| 09 | [Controlling a Village Water Tank](engineering/09-tank-level-control) | How should a pump decide how hard to work so a water tank stays at the right level, even when people suddenly use more water? |
| 10 | [Solar Power for a Home in Dangila](engineering/10-solar-energy-dangila) | How much electricity could one solar panel produce in Dangila, Ethiopia, and how does it change through the day and the year? |

## Getting started

1. Install Python 3 from python.org.
2. Install matplotlib, the one library the projects use (for charts):
   ```
   pip install matplotlib
   ```
3. Open a project folder and run its file, for example:
   ```
   cd engineering/10-solar-energy-dangila
   python solar.py
   ```

## Make it yours

These are starting points. Each project's README ends with **Try this next** ideas: pick one, change the code, and write what you found in **What I learned**. A project you extended and can explain is worth far more than one you only ran.
