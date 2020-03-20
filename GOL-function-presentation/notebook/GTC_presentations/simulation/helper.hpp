#pragma once

// checks whether the return value was successful
// If not, print an error message
inline void cuCheck(cudaError_t code){
    if(code != cudaSuccess){
        std::cerr << "Error code: " << code << std::endl << cudaGetErrorString(code) << std::endl;
    }
}

// display image in the notebook
void display_image(std::vector< unsigned char> & image, bool clear_ouput){
    // memory objects for output in the web browser
    std::stringstream buffer;
    xeus::xjson mine;

    if(clear_ouput)
        xeus::get_interpreter().clear_output(true);

    buffer.str("");
    for(auto c : image){
        buffer << c;
    }

    mine["image/png"] = xtl::base64encode(buffer.str());
    xeus::get_interpreter().display_data(
        std::move(mine),
        xeus::xjson::object(),
        xeus::xjson::object());
}
