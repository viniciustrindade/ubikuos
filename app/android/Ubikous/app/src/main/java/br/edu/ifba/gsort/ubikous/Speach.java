package br.edu.ifba.gsort.ubikous;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.net.wifi.SupplicantState;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.support.annotation.UiThread;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public class Speach extends Activity {


    private static final String TAG = "Speach";
    private TextView txtSpeechInput;
    private ImageButton btnSpeak;
    private final int REQ_CODE_SPEECH_INPUT = 100;
    Map<String, Integer> dictionary;
    private static final int EXIT = 1;
    public SpeechRecognizer sr;
    private TextToSpeech tts;
    private RequestQueue queue;
    private String ssid;
    private WifiManager wifiManager;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        queue = Volley.newRequestQueue(this);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_speach);
        txtSpeechInput = (TextView) findViewById(R.id.txtSpeechInput);
        btnSpeak = (ImageButton) findViewById(R.id.btnSpeak);



        tts = new TextToSpeech(this, new speachListener());

        // hide the action bar
        //  getActionBar().hide();
        populateDictionary();
        sr = SpeechRecognizer.createSpeechRecognizer(this);
        sr.setRecognitionListener(new recognizerListener());


        btnSpeak.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                promptSpeechInput();
            }
        });

        wifiManager = (WifiManager) getSystemService(Context.WIFI_SERVICE);





    }


    /**
     * Showing google speech input dialog
     * */
    private void promptSpeechInput() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT,
                getString(R.string.speech_prompt));
        try {
            startActivityForResult(intent, REQ_CODE_SPEECH_INPUT);
        } catch (ActivityNotFoundException a) {
            Toast.makeText(getApplicationContext(),
                    getString(R.string.speech_not_supported),
                    Toast.LENGTH_SHORT).show();
        }
    }


    /**
     * Receiving speech input
     * */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        WifiInfo wifiInfo = wifiManager.getConnectionInfo();
        if (wifiInfo.getSupplicantState() == SupplicantState.COMPLETED) {
            ssid = wifiInfo.getSSID();
        }

        switch (requestCode) {
            case REQ_CODE_SPEECH_INPUT: {
                if (resultCode == RESULT_OK && null != data) {

                    ArrayList<String> result = data
                            .getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);


                    txtSpeechInput.setText(result.get(0));

                   if (result.size() > 1){
                        String sentence = result.get(0).toLowerCase(Locale.ENGLISH).trim();
                        // Request a string response from the provided URL.
                        String url = "";
                        try {
                            ssid = URLEncoder.encode(ssid, "UTF-8");
                        } catch (UnsupportedEncodingException e) {
                            e.printStackTrace();
                        }
                        StringRequest stringRequest = new StringRequest(Request.Method.GET, "http://192.168.0.138:8080/msg-to-arduino?ssid="+ssid+"&command="+sentence,
                                new Response.Listener<String>() {
                                    @Override
                                    public void onResponse(String response) {
                                        if (response!=null) {
                                            Log.d(TAG, response + "");
                                            txtSpeechInput.setText(response);
                                            tts.speak(response, TextToSpeech.QUEUE_FLUSH, null);
                                        }

                                    }
                                }, new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {
                                if(error.getMessage()!=null) {
                                    Log.d(TAG, error.getMessage());
                                }
                                   tts.speak("Comando não encontrado", TextToSpeech.QUEUE_FLUSH, null);
                            }
                        });

                        queue.add(stringRequest);



                        Integer operation = dictionary.get(sentence);
                        if(operation != null){
                            switch(operation){
                                case EXIT:{
                                    Speach.this.finish();
                                };break;
                            }
                        }
                    }


                }
                break;
            }

        }
    }


    class recognizerListener implements RecognitionListener{


        @Override
        public void onReadyForSpeech(Bundle bundle) {

        }

        @Override
        public void onBeginningOfSpeech() {

        }

        @Override
        public void onRmsChanged(float v) {

        }

        @Override
        public void onBufferReceived(byte[] bytes) {

        }

        @Override
        public void onEndOfSpeech() {

        }

        @Override
        public void onError(int i) {

        }

        @Override
        public void onResults(Bundle results) {



            ArrayList<String> strList = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);

        }

        @Override
        public void onPartialResults(Bundle bundle) {

        }

        @Override
        public void onEvent(int i, Bundle bundle) {

        }
    }

    class speachListener implements TextToSpeech.OnInitListener{


        @Override
        public void onInit(int status) {

            if (status == TextToSpeech.SUCCESS) {
                int result = tts.setLanguage(Locale.ENGLISH);

                if (result == TextToSpeech.LANG_MISSING_DATA
                        || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                    Log.e("TTS", "This Language is not supported");
                } else {
                    btnSpeak.setEnabled(true);

                }

            } else {
                Log.e("TTS", "Initilization Failed!");
            }

        }
    }

    @Override
    public void onDestroy() {
        // Don't forget to shutdown tts!
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
        super.onDestroy();
    }



    private void populateDictionary() {
        dictionary = new HashMap<String, Integer>();
        dictionary.put("exit", EXIT);
        dictionary.put("close", EXIT);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }
}
