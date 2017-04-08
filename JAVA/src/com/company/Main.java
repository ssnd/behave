package com.company;

import com.mashape.unirest.http.HttpResponse;

import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;

import com.mashape.unirest.http.async.Callback;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import com.google.gson.Gson;

import java.util.*;

import java.util.concurrent.*;
import java.util.logging.Level;
import java.util.logging.Logger;





public class Main {
    static Map<String, String> releaseQueue = new LinkedHashMap<>();

    static ArrayList keyboardData = new ArrayList();
    static ArrayList mouseData = new ArrayList();
    static ArrayList mouseMoveData = new ArrayList();

    static String url = "http://127.0.0.1:5000/save_pc_data";

    public static final int SECOND = 1000;
    public static final String KEYBOARD_TYPE="keyboard";
    public static final String MOUSE_EVENTS_TYPE="mouse_events";
    public static final String MOUSE_MOVE_TYPE="mouse_move";


    public static Timer timer;

    public static void main(String[] args) throws InterruptedException {
        timer = new Timer();

        Logger logger = Logger.getLogger(GlobalScreen.class.getPackage().getName());
        logger.setLevel(Level.OFF);

        System.out.println("Initialized");

        try {
            GlobalScreen.registerNativeHook();
        }
        catch (NativeHookException ex) {
            System.err.println("There was a problem registering the native hook.");
            System.err.println(ex.getMessage());

            System.exit(1);
        }

        GlobalScreen.addNativeKeyListener(new KeyListener());

        MouseListener mouseListenerObject = new MouseListener();

        GlobalScreen.addNativeMouseListener(mouseListenerObject);
        GlobalScreen.addNativeMouseMotionListener(mouseListenerObject);

    }

     public static void submitData(ArrayList data, String TYPE) {
        Gson gson = new Gson();
        LinkedHashMap<String, String> submitData = new LinkedHashMap<>();


        String keyDataJson = gson.toJson(data, ArrayList.class);
        submitData.put("type", TYPE);
        submitData.put("data", keyDataJson);

        String submitJsonData = gson.toJson(submitData, LinkedHashMap.class);

        Future<HttpResponse<JsonNode>> future = Unirest.post(url)
                .header("accept", "application/json")
                .body(submitJsonData)
                .asJsonAsync(new Callback<JsonNode>() {

                     public void failed(UnirestException e) {

                     }

                     public void completed(HttpResponse<JsonNode> response) {

                         System.out.println("data successfully submitted to the server");

                     }

                     public void cancelled() {

                     }

                });

     }


    public static void rescheduleTimer() {
        timer.cancel();
        timer = new Timer();
        timer.schedule(new TimerTask() {
            public void run() {
                submitData(keyboardData, KEYBOARD_TYPE);
            }
        }, 2*SECOND);

    }



    public static void triggerPress(String keyCode, String timestamp){
        releaseQueue.put(keyCode, timestamp);
    }




    public static void triggerRelease(String keyCode, String timestamp) throws UnirestException, InterruptedException {
        LinkedHashMap<String, String> keyEventData = new LinkedHashMap<>();

        keyEventData.put("keyPress", releaseQueue.get(keyCode));
        keyEventData.put("keyRelease", timestamp);
        keyEventData.put("keyCode", keyCode);

        keyboardData.add(keyEventData);

        // here the dict reset happens (inside the rescheduleTimer method
        rescheduleTimer();


    }

    static String mouseReleaseQueue = "";


    public static void triggerMousePress(String timestamp){
        mouseReleaseQueue = timestamp;
    }

    public static void triggerMouseMove(String x, String y, String timestamp) {
        LinkedHashMap<String, String> mouseMoveEventData = new LinkedHashMap<>();

        mouseMoveEventData.put("x", Integer.valueOf(x).toString() );
        mouseMoveEventData.put("y", Integer.valueOf(y).toString() );
        mouseMoveEventData.put("timestamp", timestamp);

        mouseMoveData.add(mouseMoveEventData);

        if (mouseMoveData.size() >= 120) {
            submitData(mouseMoveData, MOUSE_MOVE_TYPE);
            mouseMoveData.clear();
        }

    }

    public static void triggerMouseRelease(String button, String timestamp){
        LinkedHashMap<String, String> mouseEventData = new LinkedHashMap<>();
        mouseEventData.put("mousePress", mouseReleaseQueue);
        mouseEventData.put("mouseRelease", timestamp);
        mouseEventData.put("buttonCode", button);
        mouseData.add(mouseEventData);


        if (mouseData.size() >= 200) {

            submitData(mouseData, MOUSE_EVENTS_TYPE);
            mouseData.clear();

        }






    }
}
