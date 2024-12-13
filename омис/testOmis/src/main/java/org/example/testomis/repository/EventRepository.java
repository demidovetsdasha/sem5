package org.example.testomis.repository;

import org.example.testomis.model.Event;
import org.example.testomis.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface EventRepository extends JpaRepository<Event, Long> {
    List<Event> findByUser(User user);

    Optional<Event> findByIdAndUser(Long id, User user);
}
