---
layout: page
permalink: /professor/
title: Professor
description: Professor profile and curriculum vitae
nav: false
nav_order: 6
_styles: >
  .professor-card {
    display: flex;
    align-items: flex-start;
    gap: 2rem;
    margin: 1rem 0 2rem 0;
    padding: 1rem;
    border: 1px solid var(--global-divider-color);
    background: rgba(255, 255, 255, 0.03);
  }
  .professor-card img {
    width: 300px;
    height: auto;
    border-radius: 6px;
  }
  .professor-card__info {
    text-align: left;
    font-size: 1.05rem;
    line-height: 1.4;
  }
  .professor-card__info p {
    margin: 0 0 0.3rem 0;
  }
  .professor-section {
    margin-top: 2rem;
  }
  .professor-section h2 {
    margin-bottom: 0.6rem;
    padding-bottom: 0.2rem;
    border-bottom: 1px solid var(--global-divider-color);
    color: #5a84c2;
    font-size: 1.8rem;
    font-weight: 700;
  }
  .professor-section h3 {
    margin: 0.9rem 0 0.3rem 0;
    font-size: 1.2rem;
    color: var(--global-text-color);
  }
  .pub-accordion {
    margin-top: 0.8rem;
  }
  .pub-accordion details {
    border: 1px solid var(--global-divider-color);
    border-radius: 6px;
    margin-bottom: 0.7rem;
    padding: 0.5rem 0.8rem;
    background: rgba(255, 255, 255, 0.02);
  }
  .pub-accordion summary {
    cursor: pointer;
    font-weight: 600;
    font-size: 1.02rem;
    margin: 0.2rem 0;
  }
  .pub-accordion details[open] summary {
    margin-bottom: 0.4rem;
  }
  .professor-section ul {
    margin: 0.3rem 0 0 1.4rem;
    padding: 0;
  }
  .professor-section li {
    margin-bottom: 0.45rem;
    line-height: 1.45;
    font-size: 1rem;
  }
  @media (max-width: 900px) {
    .professor-card {
      flex-direction: column;
    }
    .professor-card img {
      width: min(100%, 340px);
    }
  }
---

<div class="professor-card">
  <img src="{{ '/assets/img/prof_pic.jpg' | relative_url }}" alt="Myoung Hoon Lee">
  <div class="professor-card__info">
    <p><strong>Myoung Hoon Lee</strong></p>
    <p><strong>Assistant Professor</strong></p>
    <p>Department of Electrical Engineering, Incheon National University</p>
    <p>Room #251, Building 8</p>
    <p>119 Academy-ro, Yeonsu-gu, Incheon 22012, South Korea</p>
    <p>Office: (+82) 32-835-8433</p>
    <p>Email: <a href="mailto:mh.lee@inu.ac.kr">mh.lee@inu.ac.kr</a></p>
  </div>
</div>

<section class="professor-section">
  <h2>Main Fields of Research</h2>
  <ul>
    <li>Reinforcement Learning and Deep Learning</li>
    <li>Multi-Agent Optimal Control and Game Theory</li>
    <li>Unmanned Autonomous Systems Control (vehicles, drones, and robots)</li>
  </ul>
</section>

<section class="professor-section">
  <h2>Education</h2>
  <ul>
    <li>Ulsan National Institute of Science and Technology, Ulsan, South Korea (Feb. 2021)<br>Combined M.S.-Ph.D. in Electrical Engineering<br>Advisors: Jun Moon and Jin-Ho Chung<br>Thesis: <em>Game Theoretic Approaches to Decentralized Optimal Control of Unmanned Vehicles</em></li>
    <li>Kyungpook National University, Daegu, South Korea (Feb. 2016)<br>B.S. in School of Electronics Engineering</li>
  </ul>
</section>

<section class="professor-section">
  <h2>Working Experience</h2>
  <ul>
    <li>Assistant Professor, Department of Electrical Engineering, Incheon National University (Sep. 2023 - Present)</li>
    <li>Adjunct Professor, Graduate School of Manufacturing Innovation, Inha University (Sep. 2025 - Present)</li>
    <li>Postdoctoral Researcher, Research Institute of Electrical and Computer Engineering, Hanyang University (Mar. 2021 - Aug. 2023)</li>
    <li>Technical Research Personnel (Military Service), South Korea (Mar. 2020 - Feb. 2023)</li>
  </ul>
</section>

<section class="professor-section">
  <h2>Teaching Experience</h2>
  <h3>Incheon National University (Sep. 2023 - Present)</h3>
  <ul>
    <li>Fall 2025: Digital Signal Processing, System Control A, System Control B, iPBL2 (Undergraduate)</li>
    <li>Spring 2025: Linear Algebra, Signals and Systems, Introduction to Artificial Intelligence, Future Autonomous Driving System (Undergraduate)</li>
    <li>Fall 2024: Digital Control, Digital Signal Processing, Capstone Design (Undergraduate)</li>
    <li>Spring 2024: Linear Algebra, Signals and Systems (Undergraduate)</li>
    <li>Fall 2023: Digital Control, Digital Signal Processing (Undergraduate)</li>
  </ul>
  <h3>Inha University (Sep. 2025 - Present)</h3>
  <ul>
    <li>Fall 2025: Machine Learning and Reinforcement Learning for Control (Graduate)</li>
  </ul>
  <h3>Hanyang University (Mar. 2021 - Aug. 2023)</h3>
  <ul>
    <li>Fall 2022: Reinforcement Learning (Graduate)</li>
    <li>Spring 2022: Linear and Nonlinear Systems Theory (Graduate)</li>
    <li>Fall 2021: Teaching Fellow (4 weeks), Digital Logic Systems (Undergraduate)</li>
  </ul>
</section>

<section class="professor-section">
  <h2>Research Experience and Projects</h2>
  <h3>Incheon National University (Sep. 2023 - Present)</h3>
  <ul>
    <li>Research areas: Reinforcement Learning and Deep Learning; Unmanned Autonomous Systems Control</li>
    <li>Principal Investigator projects:
      <ul>
        <li>Development of AI Technology for Integrated Decision-Making and Control in Autonomous Driving Based on Multi-Objective Reinforcement Learning (NRF), Sep. 2025 - Aug. 2026</li>
        <li>Development of Fully Model-Free Reinforcement Learning Framework (INU), May 2025 - Apr. 2026</li>
        <li>Intelligent Decision-Making and Control Technologies for Autonomous Driving Based on Reinforcement Learning and Data-Driven Approaches, sub-project of Innovative Human Resource Development for Local Intellectualization (INHA University) (IITP), Apr. 2025 - Dec. 2026</li>
        <li>Development of Multi-Goal Reinforcement Learning Framework (INU), May 2024 - Apr. 2025</li>
        <li>Development of Partially-Observed Deep Reinforcement Learning Framework (INU), Sep. 2023 - Apr. 2024</li>
        <li>Development of AI for Practicality and Expertise in Real-World (NRF), Sep. 2023 - Feb. 2024</li>
      </ul>
    </li>
    <li>Co-investigator projects:
      <ul>
        <li>Development of a Demonstration-Based Robotic Platform and Network at INU Leveraging Participation in RoboCup 2026 Incheon (ITP), May 2025 - Dec. 2026</li>
        <li>Mobility Technology for Agile and Safe Autonomous Driving in Unstructured Environments (NRF), Apr. 2024 - Dec. 2027</li>
      </ul>
    </li>
  </ul>

  <h3>Hanyang University (Mar. 2021 - Aug. 2023)</h3>
  <ul>
    <li>Research areas: Reinforcement Learning and Deep Learning; Unmanned Autonomous Systems Control</li>
    <li>Principal Investigator: Development of AI for Practicality and Expertise in Real-World (NRF), Jun. 2022 - Aug. 2023</li>
    <li>Research Assistant:
      <ul>
        <li>Development of AI and Data-Driven based Integrated Autonomous Systems (NRF), Mar. 2022 - Aug. 2023</li>
        <li>Artificial Intelligence Graduate School Program, Hanyang University (IITP), Mar. 2021 - Feb. 2022</li>
      </ul>
    </li>
  </ul>

  <h3>UNIST (Mar. 2016 - Feb. 2021)</h3>
  <ul>
    <li>Research areas: Multi-Agent Optimal Control and Game Theory; Unmanned Autonomous Systems Control</li>
    <li>Research Assistant projects:
      <ul>
        <li>Development of Joint Electrical/Mechanical Drone Beamforming based on Target Detection and Precise Attitude Control (IITP), Jul. 2018 - Dec. 2020</li>
        <li>Research Center for Industry Demand Driven Aircraft Core Technology with High Efficiency and Safety (NRF), Jun. 2017 - Feb. 2019</li>
        <li>Optimal Distributed Control of Unmanned Vehicle Groups (Lockheed Martin), Jun. 2016 - Oct. 2017</li>
      </ul>
    </li>
  </ul>
</section>

<section class="professor-section">
  <h2>Publications</h2>

  <h3>Selected Publications</h3>
  <ul>
    <li>Seonjae Lee, <strong>Myoung Hoon Lee</strong>* and Jun Moon*, "Weight Vector Selection Methods by Hypervolume Maximization in the Pareto Front for Single Policy Multi-Objective Reinforcement Learning," <em>Expert Systems with Applications</em>, vol. 296, Part B, 129070, Jan. 2026.</li>
    <li>Xinfeng Sun, Haotian Zhang, <strong>Myoung Hoon Lee</strong>* and Jun Moon*, "Option-based Deep Reinforcement Learning for Topology Control of Power Systems," <em>IEEE Access</em>, vol. 13, pp. 26639-26650, Feb. 2025.</li>
    <li>Xinfeng Sun, Haotian Zhang, <strong>Myoung Hoon Lee</strong>* and Jun Moon*, "Deep Reinforcement Learning Based Active Network Management and Emergency Load-Shedding Control for Power Systems," <em>IEEE Transactions on Smart Grid</em>, vol. 15, no. 2, pp. 1423-1437, Mar. 2024.</li>
    <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Deep reinforcement learning-based model-free path planning and collision avoidance for UAVs: A soft actor-critic with hindsight experience replay approach," <em>ICT Express</em>, vol. 9, no. 3, pp. 415-419, Mar. 2023.</li>
    <li>Seonjae Lee*, <strong>Myoung Hoon Lee</strong>* and Jun Moon, "Maximum Norm Minimization: A Single-Policy Multi-Objective Reinforcement Learning to Expansion of the Pareto Front," <em>CIKM 2022</em>, Oct. 2022 (BK21 IF: 3, Co-first authors).</li>
    <li><strong>Myoung Hoon Lee</strong>, Ngo Phong Nguyen, and Jun Moon, "Leader-follower decentralized optimal control for large population hexarotors with tilted propellers: A Stackelberg game approach," <em>Journal of the Franklin Institute</em>, vol. 356, no. 12, pp. 6175-6207, Aug. 2019.</li>
  </ul>

  <h3>Full Publication List</h3>
  <div class="pub-accordion">
    <details>
      <summary>International Journals (Published and Accepted)</summary>
      <ul>
        <li>Seonjae Lee, <strong>Myoung Hoon Lee</strong>* and Jun Moon*, "Weight Vector Selection Methods by Hypervolume Maximization in the Pareto Front for Single Policy Multi-Objective Reinforcement Learning," <em>Expert Systems with Applications</em>, vol. 296, Part B, 129070, Jan. 2026.</li>
        <li>Xinfeng Sun, Haotian Zhang, <strong>Myoung Hoon Lee</strong>* and Jun Moon*, "Option-based Deep Reinforcement Learning for Topology Control of Power Systems," <em>IEEE Access</em>, vol. 13, pp. 26639-26650, Feb. 2025.</li>
        <li>Yuna Oh, <strong>Myoung Hoon Lee</strong>* and Jun Moon*, "Koopman-Based Control System for Quadrotors in Noisy Environments," <em>IEEE Access</em>, vol. 12, pp. 71675-71684, May 2024.</li>
        <li>Xinfeng Sun, Haotian Zhang, <strong>Myoung Hoon Lee</strong>* and Jun Moon*, "Deep Reinforcement Learning Based Active Network Management and Emergency Load-Shedding Control for Power Systems," <em>IEEE Transactions on Smart Grid</em>, vol. 15, no. 2, pp. 1423-1437, Mar. 2024.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Deep reinforcement learning-based model-free path planning and collision avoidance for UAVs: A soft actor-critic with hindsight experience replay approach," <em>ICT Express</em>, vol. 9, no. 3, pp. 415-419, Mar. 2023.</li>
        <li>Yuna Oh, <strong>Myoung Hoon Lee</strong> and Jun Moon, "Infinity-Norm-Based Worst-Case Collision Avoidance Control for Quadrotors," <em>IEEE Access</em>, vol. 9, pp. 101052-101064, Jul. 2021.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Backward Reachability Analysis for Nonlinear Dynamical Systems via Pseudospectral Method," <em>International Journal of Control, Automation and Systems</em>, vol. 19, pp. 575-586, Sep. 2020.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Partially-observed decentralized optimal control for large population two-wheeled vehicles: A differential game approach," <em>Journal of the Franklin Institute</em>, vol. 357, no. 9, pp. 5248-5276, Jun. 2020.</li>
        <li><strong>Myoung Hoon Lee</strong>, Ngo Phong Nguyen, and Jun Moon, "Leader-follower decentralized optimal control for large population hexarotors with tilted propellers: A Stackelberg game approach," <em>Journal of the Franklin Institute</em>, vol. 356, no. 12, pp. 6175-6207, Aug. 2019.</li>
      </ul>
    </details>

    <details>
      <summary>International Journals (Under Review)</summary>
      <ul>
        <li><strong>Myoung Hoon Lee</strong>, Yoonsoo Kim and Jun Moon, "MEGN: Maximum Entropy-Based Goal Network For Multi-Goal Reinforcement Learning," <em>ACM Transactions on Intelligent Systems and Technology</em>, under review, 2025.</li>
        <li>Xinfeng Sun, Haotian Zhang, <strong>Myoung Hoon Lee</strong>* and Jun Moon*, "TECOC: A Transformer-Enhanced Constrained Option-Critic Approach for Topology Control in Power Systems," <em>IEEE Transactions on Smart Grid</em>, under review, 2025.</li>
      </ul>
    </details>

    <details>
      <summary>Top AI Conferences</summary>
      <ul>
        <li>Seonjae Lee*, <strong>Myoung Hoon Lee</strong>* and Jun Moon, "Maximum Norm Minimization: A Single-Policy Multi-Objective Reinforcement Learning to Expansion of the Pareto Front," <em>CIKM 2022</em>, Oct. 2022 (BK21 IF: 3, Co-first authors).</li>
      </ul>
    </details>

    <details>
      <summary>International Conferences</summary>
      <ul>
        <li>Xinfeng Sun, Haotian Zhang, Jun Moon and <strong>Myoung Hoon Lee</strong>, "Constrained Variational Policy Optimization for Emergency Load Shedding of Power Systems," IFAC World Congress 2023, Jul. 2023.</li>
        <li><strong>Myoung Hoon Lee</strong>, Hyun Jong Yang and Jun Moon, "Network-Based Goal Selection for Multi-Goal Reinforcement Learning Based on Maximum Entropy Framework," ICCAS 2022, Nov. 2022.</li>
        <li>Yuna Oh, <strong>Myoung Hoon Lee</strong> and Jun Moon, "Design of Infinity-Norm Based Collision Avoidance Control System for UAVs," ASCC 2022, May 2022.</li>
        <li><strong>Myoung Hoon Lee</strong>, Jun Moon and Hyun Jong Yang, "MEGN: A Maximum Entropy Goal Selection Method for Multi-Goal Reinforcement Learning," ASCC 2022, May 2022.</li>
        <li><strong>Myoung Hoon Lee</strong>, Yoonsoo Kim, Jin-Ho Chung and Jun Moon, "Soft Actor-Critic Algorithm based Deep Reinforcement Learning for Navigation and Tracking Control of UAVs," ICCAS 2020, Oct. 2020.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Backward Reachability Analysis for Nonlinear Systems: A Pseudospectral-based Optimization Approach," ICCAS 2019, Oct. 2019.</li>
        <li><strong>Myoung Hoon Lee</strong>, Jae Hwa Lee and Jun Moon, "A Characterization of Backward Reachable Sets for Nonlinear Dynamical Systems via the Pseudospectral Legendre Method," ECC 2019, Jun. 2019.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "The Stochastic Maximum Principle for Risk-Sensitive Optimal Control with Delay and Applications," CDC 2018, Dec. 2018.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Decentralized Optimal Control for Leader-Follower Tilted-Hexarotors," ICCE Asia, Jun. 2018.</li>
        <li><strong>Myoung Hoon Lee</strong>, Kyu Taek Oh, Katherine A. Kim and Jun Moon, "Decentralized optimal control for large populations of two-wheeled vehicles," IECON 2017, Oct. 2017.</li>
      </ul>
    </details>

    <details>
      <summary>Domestic Journals</summary>
      <ul>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Soft Actor-Critic Deep Reinforcement Learning-based Navigation and Control of UAVs," <em>KIEE Magazine</em>, vol. 70, no. 4, pp. 8-14, Apr. 2021.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Decentralized Optimal Position and Attitude Control for a Group of Leader-Follower Hexarotors with Tilted Propellers," <em>Communications of KIISE</em>, vol. 37, no. 1, pp. 20-28, Jan. 2019.</li>
      </ul>
    </details>

    <details>
      <summary>Domestic Conferences</summary>
      <ul>
        <li>Seonjae Lee, <strong>Myoung Hoon Lee</strong> and Jun Moon, "Multi-Target Reinforcement Learning based Control for Autonomous Systems," ICROS, Jun. 2022.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Analysis of Backward Reachable Sets for Nonlinear Dynamical Systems via the Pseudospectral Method," ICROS, May 2019.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Decentralized Optimal Control for Leader-Follower Tilted-Hexarotors," ICROS, May 2019.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Partially-observed Decentralized Optimal Control of a Two-Wheeled Vehicles Group," ICROS, May 2019.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Large-Scale Distributed Optimal Control for Two-Wheeled Vehicles," KSAS, Nov. 2017.</li>
        <li><strong>Myoung Hoon Lee</strong> and Jun Moon, "Decentralized Control of a Two-Wheeled Vehicle Group," ICROS, May 2017.</li>
      </ul>
    </details>
  </div>

  <p><em>* indicates co-corresponding or co-first authorship as noted in each venue.</em></p>
</section>

<section class="professor-section">
  <h2>Patents</h2>
  <h3>Domestic Patents (Applications)</h3>
  <ul>
    <li>Jun Moon, Seonjae Lee, <strong>Myoung Hoon Lee</strong> and Yuna Oh, "Single-Policy Multi-Objective Reinforcement Learning method and device based on Maximum Norm minimization," No. 10-2022-0108867, Korea Patent, Aug. 30, 2022.</li>
    <li>Yuna Oh, <strong>Myoung Hoon Lee</strong> and Jun Moon, "Collision avoidance control system and method," No. 10-2022-0054912, Korea Patent, May 3, 2022.</li>
    <li><strong>Myoung Hoon Lee</strong>, Jun Moon, Hyeonsu Lyu and Hyun Jong Yang, "Autonomous Flight UAV and Method Controlling Thereof," No. 10-2021-0185112, Korea Patent, Dec. 22, 2021.</li>
  </ul>
</section>

<section class="professor-section">
  <h2>Professional Service and Invited Talks</h2>
  <h3>Reviewer</h3>
  <ul>
    <li>IEEE Transactions on Neural Networks and Learning Systems</li>
    <li>Journal of the Franklin Institute</li>
    <li>IEEE Access</li>
    <li>IEEE Transactions on Cybernetics</li>
    <li>IEEE Transactions on Vehicular Technology</li>
    <li>Autonomous Robots</li>
    <li>International Journal of Control, Automation and Systems</li>
    <li>Journal of Applied Science and Engineering</li>
    <li>IEEE Transactions on Mechatronics</li>
  </ul>
  <h3>Invited Talks and Tutorials</h3>
  <ul>
    <li>"Reinforcement Learning-Based Autonomous Driving Control," Unihub Winter Workshop, Hanyang University, Jan. 29, 2023.</li>
    <li>"Reinforcement Learning-Based Model-Free Control of AI Robots," Workshop, Incheon National University, Dec. 16, 2022.</li>
    <li>"Deep Reinforcement Learning for Autonomous Vehicle Control," Unihub Workshop, Hanyang University, Aug. 24, 2022.</li>
    <li>"Python Implementation of Sarsa and Q-learning," AI Boot Camp, Hanyang University, Feb. 9, 2022.</li>
  </ul>
</section>

<section class="professor-section">
  <h2>Awards and Honors</h2>
  <ul>
    <li>ICROS 2023 Excellent Young Researcher Award, Institute of Control, Robotics, and Systems (ICROS), Jun. 2023</li>
    <li>ICROS 2022 Best Paper Award, Institute of Control, Robotics, and Systems (ICROS), Jul. 2022</li>
    <li>Research Fellowship, Hanyang University, Mar. 2021 - Feb. 2022</li>
    <li>UNIST Scholarship, Ulsan National Institute of Science and Technology, Mar. 2016 - Feb. 2021</li>
  </ul>
</section>
