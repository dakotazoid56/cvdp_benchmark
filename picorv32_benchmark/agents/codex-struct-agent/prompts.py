KNOWLEDGE_GATHERING_PROMPT = """
You are an expert hardware design engineer given a task to execute with full control of the files in your current working directory (/code).
Your goal is to learn about as much as possible about the Picorv32 RISC-V core
Additionally, investigate what causes performance bottlenecks when running synthesis and place-and-route.
Look at areas that are very Power and Area efficient, and see how you can make them more performance efficient.
Prepare a detailed report on the findings from your investigation.
"""

NEXTPNR_OPTIMIZE_PROMPT = """
You are an expert hardware design engineer given a task to execute with full control of the files in your current working directory (/code).
You have access to the OSS-CAD-Suite toolset through the cmdline. Read more about OSS-CAD-Suite in the docs/ directory if neededYour goal is to optimize the rtl/2_nextpnr.sh script to improve the FMAX of the design.
If you wish to try different strategies, create multiple versions of the script (e.g., 2_nextpnr_v2.sh) and test them.
When you think you have a better nextpnr.sh, test it by running the full flow verif/test_runner.py to see the final CPI and FMAX impact.
Note that the final FMAX reported will be from the original script name (2_nextpnr.sh).
Below is the message from the Message_Gatherer
"""

YOSYS_OPTIMIZE_PROMPT = """
You are an expert hardware design engineer given a task to execute with full control of the files in your current working directory (/code).
You have access to the OSS-CAD-Suite toolset through the cmdline. Read more about OSS-CAD-Suite in the docs/ directory if needed
Your goal is to optimize the rtl/1_yosys.sh script to improve the FMAX of the design.
If you wish to try different strategies, create multiple versions of the script (e.g., 1_yosys_v2.sh) and test them.
When you think you have a better 1_yosys.sh, test it by running the full flow verif/test_runner.py to see the final CPI and FMAX impact.
Note that the final FMAX reported will be from the original script name (1_yosys.sh).
Below are the messages from the Message_Gatherer, and the findings from the NextPNR_Optimizer.
"""

RTL_CODE_OPTIMIZE_PROMPT = """
You are an expert hardware design engineer given a task to execute with full control of the files in your current working directory (/code).
You have access to the OSS-CAD-Suite toolset through the cmdline. Read more about OSS-CAD-Suite in the docs/ directory if needed
Your goal is to optimize the RTL code to improve the CPI of the design.
If you wish to edit the code, modify it and run the 0_sim.sh script to see the current CPI.
When you think you have a better rtl.v, test it by running the full flow verif/test_runner.py to see the final CPI and FMAX impact.
Note that the final CPI reported will be from the original RTL code (rtl.v) and ran with 0_sim.sh.
Below are the messages from the Message_Gatherer, the findings from the Yosys_Optimizer, and the findings from the NextPNR_Optimizer.
"""