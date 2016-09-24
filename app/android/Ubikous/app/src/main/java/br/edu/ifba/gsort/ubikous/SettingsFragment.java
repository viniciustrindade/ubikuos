package br.edu.ifba.gsort.ubikous;

import android.os.Bundle;
import android.preference.PreferenceFragment;

/**
 * Created by vinicius on 22/09/16.
 */
public class SettingsFragment extends PreferenceFragment {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Load the preferences from an XML resource
        addPreferencesFromResource(R.xml.preferences);

    }


    @Override
    public void onPause() {
        super.onPause();

    }
}