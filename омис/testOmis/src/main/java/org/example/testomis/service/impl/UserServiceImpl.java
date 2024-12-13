package org.example.testomis.service.impl;

import org.example.testomis.error.UserExistException;
import org.example.testomis.error.UsernameNotFoundException;
import org.example.testomis.model.User;
import org.example.testomis.payload.UserDTO;
import org.example.testomis.payload.request.SignupRequest;
import org.example.testomis.payload.response.AccessResponse;
import org.example.testomis.repository.UserRepository;
import org.example.testomis.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import java.security.Principal;

@Service
public class UserServiceImpl implements UserService {
    public static final Logger LOG = LoggerFactory.getLogger(UserServiceImpl.class);

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    @Override
    public User create(SignupRequest userIn){
        User user = new User();
        user.setEmail(userIn.getEmail());
        user.setName(userIn.getFirstname());
        user.setLastname(userIn.getLastname());
        user.setUsername(userIn.getUsername());
        user.setPassword(passwordEncoder.encode(userIn.getPassword()));
        try {
            LOG.info("Saving user {}", user.getEmail());
            return userRepository.save(user);
        }
        catch (Exception e){
            LOG.error("Error saving. {}", e.getMessage());
            throw new UserExistException("User "+ user.getEmail()+ "already exist");
        }
    }

    @Override
    public User update(UserDTO userDTO, Principal principal){
        User user = getUserByPrincipal(principal);
        user.setName(userDTO.getFirstname());
        user.setLastname(userDTO.getLastname());
        user.setBio(userDTO.getBio());
        return userRepository.save(user);
    }

    @Override
    public User getCurrent(Principal principal){
        return getUserByPrincipal(principal);
    }

    private User getUserByPrincipal(Principal principal){
        return userRepository
                .findByUsernameIgnoreCase(principal.getName())
                .orElseThrow(() -> new UsernameNotFoundException("User " + principal.getName() + " not found"));
    }

    @Override
    public User getUserById(Long id) {
        return userRepository.findById(id).orElseThrow(() -> new UsernameNotFoundException("user not found"));
    }
}
