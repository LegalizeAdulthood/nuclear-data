/ clear-set.bin
/
/ record 1
/ file offset: 0x0
        *0000
        CLR     J                       / 1510
        CLR     K                       / 1610
        CLR     JK                      / 1710
        CMP     J                       / 1520
        CMP     K                       / 1620
        CMP     JK                      / 1720
        SET     J                       / 1530
        SET     K                       / 1630
        SET     JK                      / 1730
/ checksum: 7760
