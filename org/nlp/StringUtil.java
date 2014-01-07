package org.nlp

// 一些实用的字符串处理

public class StringUtil{

    public static String findLCS (String textA, String textB){

        int[][] table = new int[textA.length()+1][textB.length()+1];
        int[][] direction = new int[textA.length()+1][textB.length()+1];

        for (int ai = 1; ai < textA.length()+1; ai++){
            for (int bi = 1; bi < textB.length()+1; bi++){
                if (textA.charAt(ai-1) == textB.charAt(bi-1)){
                    if(ai == 1 || bi == 1){
                        table[ai][bi] = 1;
                    } else {
                        table[ai][bi] = table[ai-1][bi-1] + 1;
                    }
                    direction[ai][bi] = 3;
                } else if (table[ai-1][bi] < table[ai][bi-1]){
                    table[ai][bi] = table[ai][bi-1];
                    direction[ai][bi] = 2;
                } else {
                    table[ai][bi] = table[ai-1][bi];
                    direction[ai][bi] = 1;
                }
            }
        }

        StringBuilder lcsBuilder = new StringBuilder();
        for(int ai = textA.length(), bi = textB.length(); ai > 0 && bi > 0;){
            int dir = direction[ai][bi];
            System.out.println(ai + "," + bi);
            if (dir == 3){
                lcsBuilder.append(textA.charAt(ai-1));
            }
            if ((dir & 2) == 2){
                bi--;
            }
            if ((dir & 1) == 1){
                ai--;
            }
        }

        return lcsBuilder.reverse().toString();
    }

}
