package com.company;

import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.jnativehook.keyboard.NativeKeyEvent;
import org.jnativehook.keyboard.NativeKeyListener;

public class KeyListener  implements NativeKeyListener{
    public void nativeKeyPressed(NativeKeyEvent e) {
        Main.triggerPress(String.valueOf(e.getKeyText(e.getKeyCode())),
                Long.valueOf(System.currentTimeMillis()).toString());
    }


    public void nativeKeyReleased(NativeKeyEvent e) {
        try {
            //if (e.getKeyText(e.getKeyCode()).length() == 1) {
                Main.triggerRelease(String.valueOf(e.getKeyText(e.getKeyCode())), Long.valueOf(System.currentTimeMillis()).toString());
            //}
        } catch (UnirestException e1) {
            e1.printStackTrace();
        } catch (InterruptedException e1) {
            e1.printStackTrace();
        }
    }

    public void nativeKeyTyped(NativeKeyEvent e) {
        //
    }
}