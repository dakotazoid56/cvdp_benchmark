# OSS CAD Suite

[![linux-x64](https://github.com/YosysHQ/oss-cad-suite-build/actions/workflows/linux-x64.yml/badge.svg)](https://github.com/YosysHQ/oss-cad-suite-build/releases/latest)
[![darwin-x64](https://github.com/YosysHQ/oss-cad-suite-build/actions/workflows/darwin-x64.yml/badge.svg)](https://github.com/YosysHQ/oss-cad-suite-build/releases/latest)
[![windows-x64](https://github.com/YosysHQ/oss-cad-suite-build/actions/workflows/windows-x64.yml/badge.svg)](https://github.com/YosysHQ/oss-cad-suite-build/releases/latest)

[![linux-arm64](https://github.com/YosysHQ/oss-cad-suite-build/actions/workflows/linux-arm64.yml/badge.svg)](https://github.com/YosysHQ/oss-cad-suite-build/releases/latest)
[![darwin-arm64](https://github.com/YosysHQ/oss-cad-suite-build/actions/workflows/darwin-arm64.yml/badge.svg)](https://github.com/YosysHQ/oss-cad-suite-build/releases/latest)

## Introduction

OSS CAD Suite is a binary software distribution for a number of [open source software](https://en.wikipedia.org/wiki/Open-source_software) used in digital logic design. 
You will find tools for RTL synthesis, formal hardware verification, place & route, FPGA programming, and testing with support for HDLs like Verilog, Migen, and Amaranth.

OSS CAD Suite is a component of YosysHQ's Tabby CAD Suite:  
![image](https://user-images.githubusercontent.com/59544343/119006798-f8786100-b990-11eb-9535-cef67420ccfb.png)  
See [Tabby CAD Datasheet](https://www.yosyshq.com/tabby-cad-datasheet) for details on Tabby CAD Suite; see [OSS CAD Suite GitHub](https://github.com/YosysHQ/oss-cad-suite-build/) (this page) for details on OSS CAD Suite.

### RTL Synthesis 
 * [Yosys](https://github.com/YosysHQ/yosys) RTL synthesis with extensive Verilog 2005 support
 * [Amaranth](https://github.com/amaranth-lang/amaranth) refreshed Python toolbox for building complex digital hardware
 * [Migen](https://github.com/m-labs/migen) Python toolbox for building complex digital hardware
 * [ABC](https://people.eecs.berkeley.edu/~alanmi/abc/) A System for Sequential Synthesis and Verification
 * [GHDL](https://github.com/ghdl/ghdl) VHDL 2008/93/87 simulator (linux-x64, darwin-x64 and darwin-arm64 platforms only)
 
Did you know that the Tabby CAD version of yosys supports industry standard SystemVerilog, VHDL and SVA? 
Contact us at contact@yosyshq.com to arrange a free evaluation license.

### Plugins
 * [GHDL plugin](https://github.com/ghdl/ghdl-yosys-plugin) VHDL synthesis based on GHDL (linux-x64, darwin-x64 and darwin-arm64 platforms only)
 * [Slang plugin](https://github.com/povik/yosys-slang) SystemVerilog synthesis based on Slang

### Formal Tools
 * [sby (formerly SymbiYosys)](https://github.com/YosysHQ/sby) a front-end driver program for Yosys-based formal hardware verification flows.
 * [mcy](https://github.com/YosysHQ/mcy) Mutation Cover with Yosys
 * [eqy](https://github.com/YosysHQ/eqy) Equivalence Checking with Yosys
 * [sby-gui](https://github.com/YosysHQ/sby-gui) GUI for sby (formerly SymbiYosys)
 * [aiger](https://github.com/arminbiere/aiger) AIGER tools including bounded model checker
 * [avy](https://bitbucket.org/arieg/extavy) Interpolating Property Directed Reachability tool
 * [Boolector](https://github.com/Boolector/boolector) SMT solver and BTOR model checker
 * [Yices 2](https://github.com/SRI-CSL/yices2) SMT solver
 * [Super prove](https://github.com/sterin/super-prove-build) ABC-based AIGER hardware model checker (linux-x64 platform only)
 * [Pono](https://github.com/upscale-project/pono) an SMT-based model checker built on [smt-switch](https://github.com/makaimann/smt-switch)
 * [Z3](https://github.com/Z3Prover/z3) SMT solver
 * [Bitwuzla](https://github.com/bitwuzla/bitwuzla) SMT solver

### PnR (Place and Route)
 * [nextpnr](https://github.com/YosysHQ/nextpnr) a portable FPGA place and route tool (generic, ice40, ecp5, machxo2, nexus, gowin)
 * [Project IceStorm](https://github.com/YosysHQ/icestorm) tools for working with Lattice ICE40 bitstreams
 * [Project Trellis](https://github.com/YosysHQ/prjtrellis) tools for working with Lattice ECP5 bitstreams
 * [Project Oxide](https://github.com/gatecat/prjoxide) tools for working with Lattice Nexus bitstreams
 * [Project Apicula](https://github.com/YosysHQ/apicula) tools for working with Gowin bitstreams
 * [Project Peppercorn](https://github.com/YosysHQ/prjpeppercorn) tools for working with Cologne Chip GateMate bitstreams
 
### FPGA board programming tools
 * [openFPGALoader](https://github.com/trabucayre/openFPGALoader) universal utility for programming FPGA
 * [dfu-util](http://dfu-util.sourceforge.net/) Device Firmware Upgrade Utilities
 * [ecpprog](https://github.com/gregdavill/ecpprog) basic driver for FTDI based JTAG probes, to program ECP5 FPGAs
 * [ecpdap](https://github.com/adamgreig/ecpdap) program ECP5 FPGAs and attached SPI flash using CMSIS-DAP probes in JTAG mode
 * [fujprog](https://github.com/kost/fujprog) ULX2S / ULX3S JTAG programmer
 * [openocd](http://openocd.org/) Open On-Chip Debugger
 * [icesprog](https://github.com/wuxx/icesugar/tree/master/tools/src) iCESugar FPGA board programmer
 * [iceprogduino](https://github.com/OLIMEX/iCE40HX1K-EVB/tree/master/programmer/iceprogduino) Olinuxino based programmer for iCE40HX1K-EVB
 * [TinyFPGA](https://github.com/tinyfpga/TinyFPGA-Bootloader) USB Bootloader
 * [TinyFPGA-B](https://github.com/tinyfpga/TinyFPGA-B-Series) TinyFPGA B2 Board programmer
 * [iceFUN](https://github.com/pitrz/icefunprog) iceFUN Programmer
 
### Simulation/Testing
 * [GTK Wave](https://github.com/gtkwave/gtkwave) fully featured GTK+ based wave viewer
 * [Surfer](https://gitlab.com/surfer-project/surfer) A waveform viewer with a focus on a snappy usable interface, and extensibility.
 * [verilator](https://github.com/verilator/verilator) Verilog/SystemVerilog simulator
 * [iverilog](https://github.com/steveicarus/iverilog) Verilog compilation system
 * [cocotb](https://github.com/cocotb/cocotb) coroutine based cosimulation library for writing VHDL and Verilog testbenches in Python
   
### Support libraries
 * [Python 3](https://github.com/python/cpython) language interpreter is provided in all supported platforms.
 * [Python 2](https://github.com/python/cpython) language interpreter is provided in Linux platforms in form of library only.
 * [Ubuntu 22.04](https://ubuntu.com/) distribution development packages are used and shared libraries used are provided in package.
 * [macports](https://www.macports.org/) distribution system for macOS is used to obtain all libraries used, and they are provided in package.
 * [MinGW](https://sourceforge.net/projects/mingw) Minimalist GNU for Windows library packages from Fedora 39 are used in compilation and provided in package.
 