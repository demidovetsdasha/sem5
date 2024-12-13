package org.example.testomis.service;


import org.example.testomis.model.User;
import org.example.testomis.payload.UserDTO;
import org.example.testomis.payload.request.SignupRequest;
import org.example.testomis.payload.response.AccessResponse;

import java.security.Principal;

public interface UserService {
    User create(SignupRequest userIn);

    User update(UserDTO userDTO, Principal principal);

    User getCurrent(Principal principal);

    User getUserById(Long id);
}
